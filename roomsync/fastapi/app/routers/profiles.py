from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.db import get_db
from app.models.profile import Profile, UserRole
from app.schemas.profile import (
    ProfileCreate,
    ProfileUpdate,
    ProfileResponse,
    ProfileDetail,
    ProfileSummary,
    UserRoleEnum,
)
from app.dependencies.auth import get_current_user, require_admin


router = APIRouter(prefix="/profiles", tags=["Profiles"])


# ════════════════════════════════════════════════════════════════════════════
# GET /profiles/ - ดึง Profile ทั้งหมด (Admin only)
# ════════════════════════════════════════════════════════════════════════════
@router.get("/", response_model=List[ProfileResponse])
def get_all_profiles(
    skip: int = 0,
    limit: int = 100,
    role: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_admin)
):
    """
    ดึงรายการ Profile ทั้งหมด (Admin only)
    
    - **skip**: ข้ามกี่รายการ (pagination)
    - **limit**: จำกัดจำนวน (pagination)
    - **role**: filter ตาม role (admin, teacher, student)
    """
    query = db.query(Profile)
    
    if role:
        query = query.filter(Profile.role == role)
    
    return query.order_by(Profile.created_at.desc()).offset(skip).limit(limit).all()


# ════════════════════════════════════════════════════════════════════════════
# GET /profiles/summary - สรุปจำนวน Users (Admin only)
# ════════════════════════════════════════════════════════════════════════════
@router.get("/summary", response_model=ProfileSummary)
def get_profile_summary(
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_admin)
):
    """ดึงสรุปจำนวน Users ตาม Role (Admin only)"""
    
    from sqlalchemy import func
    
    total = db.query(func.count(Profile.id)).scalar()
    admin_count = db.query(func.count(Profile.id)).filter(
        Profile.role == UserRole.ADMIN.value
    ).scalar()
    teacher_count = db.query(func.count(Profile.id)).filter(
        Profile.role == UserRole.TEACHER.value
    ).scalar()
    student_count = db.query(func.count(Profile.id)).filter(
        Profile.role == UserRole.STUDENT.value
    ).scalar()
    
    return ProfileSummary(
        total=total,
        admin=admin_count,
        teacher=teacher_count,
        student=student_count
    )


# ════════════════════════════════════════════════════════════════════════════
# GET /profiles/me - ดึงข้อมูลตัวเอง
# ════════════════════════════════════════════════════════════════════════════
@router.get("/me", response_model=ProfileResponse)
def get_my_profile(current_user: Profile = Depends(get_current_user)):
    """ดึงข้อมูล Profile ของตัวเอง"""
    return current_user


# ════════════════════════════════════════════════════════════════════════════
# GET /profiles/check/{auth_user_id} - เช็คว่ามี Profile หรือยัง
# ════════════════════════════════════════════════════════════════════════════
@router.get("/check/{auth_user_id}", response_model=ProfileResponse)
def check_profile_exists(
    auth_user_id: UUID,
    db: Session = Depends(get_db)
):
    """
    เช็คว่า auth_user_id นี้มี Profile หรือยัง
    
    ใช้หลังจาก Supabase Auth signup เพื่อเช็คว่าต้องสร้าง Profile ไหม
    """
    profile = db.query(Profile).filter(Profile.auth_user_id == auth_user_id).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    return profile


# ════════════════════════════════════════════════════════════════════════════
# GET /profiles/{profile_id} - ดึง Profile ตาม ID (Admin only)
# ════════════════════════════════════════════════════════════════════════════
@router.get("/{profile_id}", response_model=ProfileResponse)
def get_profile(
    profile_id: UUID,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_admin)
):
    """ดึงข้อมูล Profile ตาม ID (Admin only)"""
    
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    return profile


# ════════════════════════════════════════════════════════════════════════════
# POST /profiles/ - สร้าง Profile ใหม่
# ════════════════════════════════════════════════════════════════════════════
@router.post("/", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
def create_profile(
    profile_data: ProfileCreate,
    db: Session = Depends(get_db)
):
    """
    สร้าง Profile ใหม่ (เรียกหลังจาก Supabase Auth signup)
    
    Note: 
    - ปกติจะใช้ Supabase trigger สร้างอัตโนมัติ
    - endpoint นี้ไว้สำหรับกรณีที่ต้องสร้างเอง
    - ไม่ต้อง login ก็สร้างได้ (เพราะสร้างหลัง signup)
    """
    
    # เช็คว่า auth_user_id ซ้ำไหม
    existing = db.query(Profile).filter(
        Profile.auth_user_id == profile_data.auth_user_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile already exists for this user"
        )
    
    profile = Profile(
        auth_user_id=profile_data.auth_user_id,
        first_name=profile_data.first_name,
        last_name=profile_data.last_name,
        role=profile_data.role.value  # แปลง Enum เป็น string
    )
    
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


# ════════════════════════════════════════════════════════════════════════════
# PUT /profiles/me - อัพเดท Profile ของตัวเอง
# ════════════════════════════════════════════════════════════════════════════
@router.put("/me", response_model=ProfileResponse)
def update_my_profile(
    profile_data: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(get_current_user)
):
    """
    อัพเดท Profile ของตัวเอง
    
    ⚠️ User ทั่วไปไม่สามารถเปลี่ยน role ตัวเองได้
    """
    
    update_data = profile_data.model_dump(exclude_unset=True)
    
    # User ทั่วไปไม่สามารถเปลี่ยน role ตัวเองได้
    if 'role' in update_data:
        del update_data['role']
    
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    return current_user


# ════════════════════════════════════════════════════════════════════════════
# PUT /profiles/{profile_id} - อัพเดท Profile (Admin only)
# ════════════════════════════════════════════════════════════════════════════
@router.put("/{profile_id}", response_model=ProfileResponse)
def update_profile(
    profile_id: UUID,
    profile_data: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_admin)
):
    """
    อัพเดท Profile (Admin only)
    
    Admin สามารถเปลี่ยน role ได้
    """
    
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    update_data = profile_data.model_dump(exclude_unset=True)
    
    # แปลง Enum เป็น string ถ้ามี role
    if 'role' in update_data and update_data['role']:
        update_data['role'] = update_data['role'].value
    
    for field, value in update_data.items():
        setattr(profile, field, value)
    
    profile.updated_by = current_user.auth_user_id
    
    db.commit()
    db.refresh(profile)
    return profile


# ════════════════════════════════════════════════════════════════════════════
# PATCH /profiles/{profile_id}/role - เปลี่ยน Role (Admin only)
# ════════════════════════════════════════════════════════════════════════════
@router.patch("/{profile_id}/role", response_model=ProfileResponse)
def change_user_role(
    profile_id: UUID,
    role: UserRoleEnum,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_admin)
):
    """
    เปลี่ยน Role ของ User (Admin only)
    
    ใช้ตอนต้องการเปลี่ยน role อย่างเดียว เช่น:
    - เปลี่ยน student → teacher
    - เปลี่ยน teacher → admin
    """
    
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    # ป้องกันไม่ให้เปลี่ยน role ตัวเอง
    if profile.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change your own role"
        )
    
    profile.role = role.value
    profile.updated_by = current_user.auth_user_id
    
    db.commit()
    db.refresh(profile)
    return profile


# ════════════════════════════════════════════════════════════════════════════
# DELETE /profiles/{profile_id} - ลบ Profile (Admin only)
# ════════════════════════════════════════════════════════════════════════════
@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(
    profile_id: UUID,
    db: Session = Depends(get_db),
    current_user: Profile = Depends(require_admin)
):
    """
    ลบ Profile (Admin only)
    
    ⚠️ ไม่สามารถลบตัวเองได้
    ⚠️ ควรลบ Supabase Auth user ด้วย (ทำที่ Frontend หรือ Supabase trigger)
    """
    
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    # ป้องกันไม่ให้ลบตัวเอง
    if profile.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete yourself"
        )
    
    db.delete(profile)
    db.commit()
