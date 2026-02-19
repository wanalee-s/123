from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional

from app.db import get_db
from app.models.profile import Profile, UserRole


# ════════════════════════════════════════════════════════════════════════════
# GET CURRENT USER - ดึง Profile จาก Header
# ════════════════════════════════════════════════════════════════════════════
def get_current_user(
    auth_user_id: UUID = Header(..., alias="X-Auth-User-ID"),
    db: Session = Depends(get_db)
) -> Profile:
    """
    ดึง Profile ปัจจุบันจาก X-Auth-User-ID header
    
    Frontend ต้องส่ง header:
    X-Auth-User-ID: <supabase-auth-user-id>
    
    ถ้าไม่ส่ง หรือหาไม่เจอ → 401 Unauthorized
    """
    
    profile = db.query(Profile).filter(
        Profile.auth_user_id == auth_user_id
    ).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Profile not found. Please create profile first."
        )
    
    return profile


# ════════════════════════════════════════════════════════════════════════════
# GET CURRENT USER (OPTIONAL) - ไม่บังคับ login
# ════════════════════════════════════════════════════════════════════════════
def get_current_user_optional(
    auth_user_id: Optional[UUID] = Header(None, alias="X-Auth-User-ID"),
    db: Session = Depends(get_db)
) -> Optional[Profile]:
    """
    ดึง Profile ปัจจุบัน (ไม่บังคับ login)
    
    ใช้สำหรับ endpoint ที่ไม่บังคับ login แต่ถ้า login จะแสดงข้อมูลเพิ่ม
    """
    
    if not auth_user_id:
        return None
    
    return db.query(Profile).filter(
        Profile.auth_user_id == auth_user_id
    ).first()


# ════════════════════════════════════════════════════════════════════════════
# REQUIRE ADMIN - ต้องเป็น Admin
# ════════════════════════════════════════════════════════════════════════════
def require_admin(
    current_user: Profile = Depends(get_current_user)
) -> Profile:
    """
    ต้องเป็น Admin เท่านั้น
    
    ถ้าไม่ใช่ Admin → 403 Forbidden
    """
    
    if not current_user.is_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return current_user


# ════════════════════════════════════════════════════════════════════════════
# REQUIRE ADMIN OR TEACHER
# ════════════════════════════════════════════════════════════════════════════
def require_admin_or_teacher(
    current_user: Profile = Depends(get_current_user)
) -> Profile:
    """
    ต้องเป็น Admin หรือ Teacher
    
    ใช้สำหรับ endpoint ที่ทั้ง Admin และ Teacher ใช้ได้
    """
    
    if current_user.role not in [UserRole.ADMIN.value, UserRole.TEACHER.value]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin or Teacher access required"
        )
    
    return current_user


# ════════════════════════════════════════════════════════════════════════════
# REQUIRE OWNER OR ADMIN - ต้องเป็นเจ้าของหรือ Admin
# ════════════════════════════════════════════════════════════════════════════
def check_owner_or_admin(
    current_user: Profile,
    owner_id: UUID
) -> bool:
    """
    เช็คว่าเป็นเจ้าของหรือ Admin
    
    ใช้ใน Router:
    if not check_owner_or_admin(current_user, booking.user_id):
        raise HTTPException(403, "Access denied")
    """
    
    if current_user.is_admin():
        return True
    
    if current_user.auth_user_id == owner_id:
        return True
    
    return False