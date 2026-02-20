#!/usr/bin/env python3
# fastapi/app/routers/auth.py

import logging
import secrets
from urllib import request
from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.auth import UserResponse, Message, UserRegister, UserLogin, Token

from app.models.authuser import AuthUser
from app.config import settings
from jose import jwt, JWTError
from datetime import datetime, timedelta
from httpx import AsyncClient
from passlib.context import CryptContext

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set this logger to DEBUG

router = APIRouter()

# Password hashing context  
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration
SECRET_KEY = settings.jwt_secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 1 day (1440 minutes)

GOOGLE_REDIRECT_URI = "http://localhost:8080/auth/google/auth"  # Adjust as needed
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"
GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_URL = "https://api.github.com/user"
GITHUB_EMAILS_URL = "https://api.github.com/user/emails"


# Check if Google OAuth credentials are set in environment variables
def get_google_oauth_config() -> tuple[str, str]:
    client_id = settings.google_client_id
    client_secret = settings.google_client_secret
    if not client_id or not client_secret:
        raise HTTPException(status_code=500, detail="Google OAuth is not configured")
    return client_id, client_secret


# Check if GitHub OAuth credentials are set in environment variables
def get_github_oauth_config() -> tuple[str, str]:
    client_id = settings.github_client_id
    client_secret = settings.github_client_secret
    if not client_id or not client_secret:
        raise HTTPException(status_code=500, detail="GitHub OAuth is not configured")
    return client_id, client_secret

# Fetch GitHub profile information using the access token
async def fetch_github_profile(access_token: str) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github+json",
    }
    async with AsyncClient() as client:
        user_response = await client.get(GITHUB_USER_URL, headers=headers)
        user_data = user_response.json()
        email = user_data.get("email")
        if not email:
            emails_response = await client.get(GITHUB_EMAILS_URL, headers=headers)
            emails = emails_response.json()
            primary = next((e for e in emails if e.get("primary") and e.get("verified")), None)
            email = primary.get("email") if primary else None
        return {
            "email": email,
            "name": user_data.get("name") or user_data.get("login"),
            "avatar_url": user_data.get("avatar_url"),
            "login": user_data.get("login"),
        }

# Utility function to create JWT tokens
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    csrf_token = secrets.token_hex(16)
    to_encode["csrf_token"] = csrf_token
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

# Dependency to get the current user from the JWT token
async def get_current_user(request: Request, db: Session = Depends(get_db)):
    logger.debug(f"Checking JWT cookie in get_current_user")
    token = request.cookies.get("jwt")
    logger.debug(f"JWT cookie: {token}")
    if not token:
        logger.error("Missing JWT cookie in get_current_user")
        raise HTTPException(status_code=401, detail="Missing JWT cookie")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.debug(f"JWT payload: {payload}")
        user_id: str = payload.get("sub")
        logger.debug(f"Extracted user_id from sub: {user_id}")
        if user_id is None:
            logger.error("Invalid token: subject missing")
            raise HTTPException(
                status_code=401, detail="Invalid token: subject missing")
        user = db.query(AuthUser).filter(AuthUser.id == int(user_id)).first()
        if user is None:
            logger.error(f"User not found for id: {user_id}")
            raise HTTPException(status_code=401, detail="User not found")
        logger.debug(f"User found: {user.email}")
        return user
    except JWTError as e:
        logger.error(f"JWT decoding failed: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")

# Check if auth router is working
@router.get("/", response_model=Message)
async def hello():
    """
    **Root Auth Endpoint**

    Returns a simple greeting message to verify the auth router is active.
    """
    logger.info("Auth hello endpoint accessed")
    return {"message": "From auth.py: Hello World!"}

# route to check if credentials are loaded properly (for debugging)
@router.get("/debug")
async def debug():
    """Debug endpoint to check if credentials are loaded"""
    client_id = settings.google_client_id
    client_secret = settings.google_client_secret
    github_id = settings.github_client_id
    github_secret = settings.github_client_secret
    
    return {
        "google_client_id": client_id,
        "google_client_secret": client_secret[:10] + "***" if client_secret else None,
        "github_client_id": github_id,
        "github_client_secret": github_secret[:10] + "***" if github_secret else None,
        "redirect_uri_template": "Will be generated at login"
    }

# Registration and Login Endpoints
@router.post("/register", response_model=UserResponse)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user with email and password"""
    if db.query(AuthUser).filter(AuthUser.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pwd = pwd_context.hash(user_data.password)
    user = AuthUser(
        email=user_data.email,
        name=user_data.name,
        password_hash=hashed_pwd
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Login with email/password
@router.post("/login/email", response_model=Token)
async def login_email(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login with email/password"""
    user = db.query(AuthUser).filter(AuthUser.email == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.password_hash or ""):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(data={"sub": str(user.id), "email": user.email})
    return {"access_token": token, "token_type": "bearer"}

# OAuth Endpoints
@router.get("/login", response_description="Redirects to Google OAuth")
async def login(request: Request):
    """
    **Initiate Google OAuth Login**

    Constructs the Google OAuth URL with identifying scopes (openid, email, profile)
    and redirects the user to Google's consent page.
    """
    # ... implementation details ...
    client_id, _ = get_google_oauth_config()
    redirect_uri = str(request.url_for("google_auth"))
    auth_url = (
        f"{GOOGLE_AUTH_URL}?response_type=code&client_id={client_id}"
        f"&redirect_uri={redirect_uri}&scope=openid%20email%20profile"
    )
    logger.info("Redirecting to Google OAuth")
    return RedirectResponse(url=auth_url)


# GitHub OAuth Login Endpoint
@router.get("/login/github", response_description="Redirects to GitHub OAuth")
async def github_login(request: Request):
    client_id, _ = get_github_oauth_config()
    redirect_uri = str(request.url_for("github_auth"))
    auth_url = (
        f"{GITHUB_AUTH_URL}?client_id={client_id}"
        f"&redirect_uri={redirect_uri}&scope=read:user%20user:email"
    )
    logger.info("Redirecting to GitHub OAuth")
    return RedirectResponse(url=auth_url)
    

# Google OAuth Callback Endpoint
@router.get("/google/auth", name="google_auth", response_description="Redirects to Frontend with JWT")
async def google_auth(request: Request, db: Session = Depends(get_db)):
    """
    **Google OAuth Callback**

    Handles the callback from Google:
    1. Exchanges the authorization code for an access token.
    2. Fetches user profile information from Google.
    3. Creates or updates the user in the local database.
    4. Generates a valid JWT for the session.
    5. Redirects the user back to the frontend with the JWT query parameter.
    """
    # ... implementation details ...
    try:
        client_id, client_secret = get_google_oauth_config()
        code = request.query_params.get("code")
    # ... rest of the function ...
        # (This is a large block, I will strictly follow replacement rules in next step, 
        # simplifying here for the thought process)
        if not code:
            raise ValueError("No authorization code provided")

        async with AsyncClient() as client:
            token_response = await client.post(
                GOOGLE_TOKEN_URL,
                data={
                    "code": code,
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "redirect_uri": str(request.url_for("google_auth")),
                    "grant_type": "authorization_code",
                },
            )
            token_data = token_response.json()
            if "error" in token_data:
                raise ValueError(f"Google OAuth error: {token_data['error']}")
            access_token = token_data.get("access_token")

            user_info_response = await client.get(
                GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {access_token}"},
            )
            user_info = user_info_response.json()
            logger.debug(f"Google profile: {user_info}")

        user = db.query(AuthUser).filter(
            AuthUser.email == user_info["email"]).first()
        if not user:
            logger.debug("User not found, creating one")
            user = AuthUser(
                email=user_info["email"],
                name=user_info["name"],
                avatar_url=user_info.get("picture")
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            logger.debug("User found, updating details")
            user.name = user_info["name"]
            user.avatar_url = user_info.get("picture")
            db.commit()

        jwt_token = create_access_token(
            data={"sub": str(user.id), "name": user.name,
                  "email": user.email, "avatar_url": user.avatar_url},
            expires_delta=timedelta(days=1)
        )
        frontend_url = settings.frontend_login_success_uri
        logger.info(f"Redirecting to frontend with token for {user.email}")
        return RedirectResponse(url=f"{frontend_url}?token={jwt_token}")

    except Exception as e:
        logger.error(f"Error processing Google auth callback: {e}")
        return RedirectResponse(url=settings.frontend_login_failure_uri)


# GitHub OAuth Callback Endpoint
@router.get("/github/auth", name="github_auth", response_description="Redirects to Frontend with JWT")
async def github_auth(request: Request, db: Session = Depends(get_db)):
    try:
        client_id, client_secret = get_github_oauth_config()
        code = request.query_params.get("code")
        if not code:
            raise ValueError("No authorization code provided")

        async with AsyncClient() as client:
            token_response = await client.post(
                GITHUB_TOKEN_URL,
                data={
                    "code": code,
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "redirect_uri": str(request.url_for("github_auth")),
                },
                headers={"Accept": "application/json"},
            )
            token_data = token_response.json()
            if "error" in token_data:
                raise ValueError(f"GitHub OAuth error: {token_data['error']}")
            access_token = token_data.get("access_token")
            if not access_token:
                raise ValueError("No access token returned from GitHub")

        profile = await fetch_github_profile(access_token)
        email = profile.get("email")
        if not email:
            login = profile.get("login") or "user"
            email = f"{login}@users.noreply.github.com"

        user = db.query(AuthUser).filter(AuthUser.email == email).first()
        if not user:
            logger.debug("User not found, creating one")
            user = AuthUser(
                email=email,
                name=profile.get("name"),
                avatar_url=profile.get("avatar_url"),
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            logger.debug("User found, updating details")
            user.name = profile.get("name")
            user.avatar_url = profile.get("avatar_url")
            db.commit()

        jwt_token = create_access_token(
            data={"sub": str(user.id), "name": user.name,
                  "email": user.email, "avatar_url": user.avatar_url},
            expires_delta=timedelta(days=1)
        )
        frontend_url = settings.frontend_login_success_uri
        logger.info(f"Redirecting to frontend with token for {user.email}")
        return RedirectResponse(url=f"{frontend_url}?token={jwt_token}")

    except Exception as e:
        logger.error(f"Error processing GitHub auth callback: {e}")
        return RedirectResponse(url=settings.frontend_login_failure_uri)


# Logout Endpoint
@router.get("/logout", response_model=Message)
async def logout():
    """
    **Logout User**

    Instructs the client to clear the JWT token.
    Note: Real server-side logout would require a token blacklist.
    """
    logger.info("User logged out")
    return JSONResponse(content={"message": "Logout successful. Remove JWT token on frontend."})


# Protected Endpoint to Get Current User Profile
@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: AuthUser = Depends(get_current_user)):
    """
    **Get Current User Profile**

    Returns the profile information of the currently authenticated user.
    Requires a valid JWT token in the `jwt` cookie or Authorization header (logic depends on `get_current_user`).
    """
    logger.info(f"Fetching profile for {current_user.email}")
    return {"email": current_user.email, "name": current_user.name, "avatar_url": current_user.avatar_url}

# Utility function to register routes in the main app
def register_routes(router_instance: APIRouter):
    router_instance.include_router(router)

