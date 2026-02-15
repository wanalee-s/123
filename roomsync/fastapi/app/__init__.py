# fastapi/app/__init__.py
from fastapi import FastAPI, APIRouter, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.db import Base, engine
from app.routers import auth, phonebook
from app.env_detector import should_auto_create_tables
import logging
import os
from fastapi.responses import JSONResponse
from jose import JWTError
from jose.exceptions import ExpiredSignatureError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request as StarletteRequest
from jose import jwt

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("app")

# Detect if running on Vercel (Vercel sets VERCEL=1 automatically)
api_prefix = "/api" if os.getenv("VERCEL") else ""
logger.info(f"Running with api_prefix: '{api_prefix}' (VERCEL={os.getenv('VERCEL')})")

fastapi_app = FastAPI(
    title="FastAPI Backend",
    debug=settings.debug,
    docs_url=f"{api_prefix}/docs",
    redoc_url=f"{api_prefix}/redoc",
    openapi_url=f"{api_prefix}/openapi.json"
)
fastapi_app.logger = logger

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class JWTAndCSRFMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: StarletteRequest, call_next):
        excluded_paths = ["/", "/login", "/google/auth", "/logout"]
        logger.debug(f"Request method: {request.method}, path: {request.url.path}")
        if request.method not in ["POST", "PUT", "DELETE"] or request.url.path in excluded_paths:
            logger.debug("Skipping JWT/CSRF validation for this request")
            return await call_next(request)

        token = request.cookies.get("jwt")
        logger.debug(f"JWT cookie: {token}")
        if not token:
            logger.error("Missing JWT cookie in middleware")
            raise HTTPException(status_code=401, detail="Missing JWT cookie")

        try:
            payload = jwt.decode(
                token, settings.jwt_secret_key, algorithms=["HS256"])
            logger.debug(f"JWT payload: {payload}")
        except JWTError as e:
            logger.error(f"JWT decoding failed in middleware: {e}")
            raise HTTPException(
                status_code=401, detail="Invalid or expired token")

        client_csrf = request.headers.get("X-CSRF-Token")
        logger.debug(f"Client CSRF token: {client_csrf}")
        if not client_csrf or payload.get("csrf_token") != client_csrf:
            logger.error("CSRF token mismatch in middleware")
            raise HTTPException(status_code=403, detail="CSRF token mismatch")

        response = await call_next(request)
        return response


fastapi_app.add_middleware(JWTAndCSRFMiddleware)
fastapi_app.state.settings = settings

# Auto-detect environment and conditionally create tables
try:
    if should_auto_create_tables():
        logger.info("Auto-creating database tables (Docker)")
        Base.metadata.create_all(bind=engine)
    else:
        logger.info("Skipping table creation (Vercel/Local)")
except Exception as e:
    logger.error(f"Error during table creation: {e}")
    # Don't fail the app if table creation fails

auth_router = APIRouter()
auth.register_routes(auth_router)
fastapi_app.include_router(auth_router, prefix=api_prefix, tags=["Auth"])
fastapi_app.include_router(
    phonebook.router, prefix=f"{api_prefix}/lab10", tags=["Phonebook"])


@fastapi_app.exception_handler(JWTError)
async def jwt_error_handler(request: Request, exc: JWTError):
    fastapi_app.logger.error(f"JWT Error: {exc}")
    return JSONResponse(status_code=401, content={"error": "Invalid token"})


@fastapi_app.exception_handler(ExpiredSignatureError)
async def jwt_expired_error_handler(request: Request, exc: ExpiredSignatureError):
    fastapi_app.logger.error(f"JWT Expired Token Error: {exc}")
    return JSONResponse(status_code=401, content={"error": "Token expired"})

fastapi_app.logger.info(f"Starting FastAPI app with DATABASE_URL: {settings.database_url}")
fastapi_app.logger.debug(f"Allowed origins: {settings.allowed_origins}")
