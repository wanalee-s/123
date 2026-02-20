from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ════════════════════════════════════════════════════════════════════════════
# Import Routers
# ════════════════════════════════════════════════════════════════════════════
from app.routers.profiles import router as profiles_router
from app.routers.rooms import router as rooms_router
from app.routers.equipments import router as equipments_router
from app.routers.room_equipments import router as room_equipments_router
from app.routers.bookings import router as bookings_router
from app.routers.damage_reports import router as damage_reports_router


# ════════════════════════════════════════════════════════════════════════════
# Create FastAPI Application
# ════════════════════════════════════════════════════════════════════════════
app = FastAPI(
    title="RoomSync API",
    description="API สำหรับระบบจองห้อง RoomSync",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


# ════════════════════════════════════════════════════════════════════════════
# CORS Middleware
# ════════════════════════════════════════════════════════════════════════════
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # อนุญาตทุก origin (production ควรระบุเฉพาะ)
    allow_credentials=True,
    allow_methods=["*"],  # อนุญาตทุก HTTP methods
    allow_headers=["*"],  # อนุญาตทุก headers
)


# ════════════════════════════════════════════════════════════════════════════
# Include Routers
# ════════════════════════════════════════════════════════════════════════════
app.include_router(profiles_router, prefix="/api/v1")
app.include_router(rooms_router, prefix="/api/v1")
app.include_router(equipments_router, prefix="/api/v1")
app.include_router(room_equipments_router, prefix="/api/v1")
app.include_router(bookings_router, prefix="/api/v1")
app.include_router(damage_reports_router, prefix="/api/v1")


# ════════════════════════════════════════════════════════════════════════════
# Root Endpoints
# ════════════════════════════════════════════════════════════════════════════
@app.get("/")
def root():
    """หน้าแรกของ API"""
    return {
        "message": "Welcome to RoomSync API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    """เช็คสถานะ API (สำหรับ monitoring)"""
    return {"status": "healthy"}