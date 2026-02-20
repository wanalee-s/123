from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime
from enum import Enum


# ════════════════════════════════════════════════════════════════════════════
# ENUM - Role ของผู้ใช้
# ════════════════════════════════════════════════════════════════════════════
class UserRoleEnum(str, Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"


# ════════════════════════════════════════════════════════════════════════════
# CREATE SCHEMA - ใช้ตอนสร้าง Profile ใหม่
# ════════════════════════════════════════════════════════════════════════════
class ProfileCreate(BaseModel):
    auth_user_id: UUID
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    role: UserRoleEnum = UserRoleEnum.STUDENT


# ════════════════════════════════════════════════════════════════════════════
# UPDATE SCHEMA - ใช้ตอนแก้ไข Profile
# ════════════════════════════════════════════════════════════════════════════
class ProfileUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    role: Optional[UserRoleEnum] = None


# ════════════════════════════════════════════════════════════════════════════
# RESPONSE SCHEMA - ใช้ตอบกลับ
# ════════════════════════════════════════════════════════════════════════════
class ProfileResponse(BaseModel):
    id: UUID
    auth_user_id: UUID
    first_name: str
    last_name: str
    role: str
    created_at: datetime
    updated_at: datetime
    created_by: Optional[UUID] = None
    updated_by: Optional[UUID] = None

    class Config:
        from_attributes = True


# ════════════════════════════════════════════════════════════════════════════
# DETAIL SCHEMA - Response พร้อมข้อมูลเพิ่มเติม
# ════════════════════════════════════════════════════════════════════════════
class ProfileDetail(ProfileResponse):
    full_name: str
    display_name: str


# ════════════════════════════════════════════════════════════════════════════
# SUMMARY SCHEMA - สรุปจำนวน Users ตาม Role (สำหรับ Dashboard)
# ════════════════════════════════════════════════════════════════════════════
class ProfileSummary(BaseModel):
    total: int
    admin: int
    teacher: int
    student: int