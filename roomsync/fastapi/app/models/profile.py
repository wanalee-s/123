"""
 หน้าที่:                                                                   │
│  1. เก็บข้อมูลผู้ใช้ (ชื่อ, นามสกุล)                                         │
│  2. เชื่อมกับ Supabase Auth (auth_user_id)                                  │
│  3. กำหนด Role (admin, teacher, student)                                    │
│  4. ใช้ตรวจสอบสิทธิ์การเข้าถึง
"""


from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from app.db import Base


# ════════════════════════════════════════════════════════════════════════════
# ENUM - Role ของผู้ใช้
# ════════════════════════════════════════════════════════════════════════════
class UserRole(str, enum.Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"


# ════════════════════════════════════════════════════════════════════════════
# PROFILE MODEL
# ════════════════════════════════════════════════════════════════════════════
class Profile(Base):
    """Model สำหรับตาราง profiles (เชื่อมกับ Supabase Auth)"""
    
    __tablename__ = "profiles"

    # ════════════════════════════════════════════════════════════════
    # PRIMARY KEY
    # ════════════════════════════════════════════════════════════════
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # ════════════════════════════════════════════════════════════════
    # SUPABASE AUTH LINK
    # ════════════════════════════════════════════════════════════════
    auth_user_id = Column(
        UUID(as_uuid=True), 
        unique=True, 
        nullable=False, 
        index=True
    )

    # ════════════════════════════════════════════════════════════════
    # USER INFO
    # ════════════════════════════════════════════════════════════════
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)

    # ════════════════════════════════════════════════════════════════
    # ROLE
    # ════════════════════════════════════════════════════════════════
    role = Column(Text, default=UserRole.STUDENT.value, nullable=False)

    # ════════════════════════════════════════════════════════════════
    # TIMESTAMPS
    # ════════════════════════════════════════════════════════════════
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    # ════════════════════════════════════════════════════════════════
    # AUDIT FIELDS
    # ════════════════════════════════════════════════════════════════
    created_by = Column(UUID(as_uuid=True), nullable=True)
    updated_by = Column(UUID(as_uuid=True), nullable=True)

    # ════════════════════════════════════════════════════════════════
    # RELATIONSHIPS
    # ════════════════════════════════════════════════════════════════
    # One-to-Many: Profile can have many Bookings
    bookings = relationship("Booking", back_populates="profile", cascade="all, delete-orphan")

    # ════════════════════════════════════════════════════════════════
    # METHODS - String Representation
    # ════════════════════════════════════════════════════════════════
    def __repr__(self):
        return f"<Profile {self.first_name} {self.last_name} ({self.role})>"

    # ════════════════════════════════════════════════════════════════
    # METHODS - Role Checking
    # ════════════════════════════════════════════════════════════════
    def is_admin(self) -> bool:
        """เช็คว่าเป็น Admin ไหม"""
        return self.role == UserRole.ADMIN.value

    def is_teacher(self) -> bool:
        """เช็คว่าเป็น Teacher ไหม"""
        return self.role == UserRole.TEACHER.value

    def is_student(self) -> bool:
        """เช็คว่าเป็น Student ไหม"""
        return self.role == UserRole.STUDENT.value

    # ════════════════════════════════════════════════════════════════
    # METHODS - Permission Checking
    # ════════════════════════════════════════════════════════════════
    def can_auto_approve_booking(self) -> bool:
        """
        เช็คว่าจองห้องได้เลยไหม (ไม่ต้องรออนุมัติ)
        - Admin และ Teacher → จองได้เลย
        - Student → ต้องรออนุมัติ
        """
        return self.role in [UserRole.ADMIN.value, UserRole.TEACHER.value]

    def can_manage_rooms(self) -> bool:
        """เช็คว่าจัดการห้องได้ไหม (สร้าง/แก้ไข/ลบ)"""
        return self.role == UserRole.ADMIN.value

    def can_manage_equipments(self) -> bool:
        """เช็คว่าจัดการอุปกรณ์ได้ไหม"""
        return self.role == UserRole.ADMIN.value

    def can_approve_bookings(self) -> bool:
        """เช็คว่าอนุมัติ/ปฏิเสธ การจองได้ไหม"""
        return self.role == UserRole.ADMIN.value

    def can_manage_damage_reports(self) -> bool:
        """เช็คว่าจัดการ Damage Reports ได้ไหม (เปลี่ยนสถานะ)"""
        return self.role == UserRole.ADMIN.value

    def can_view_all_bookings(self) -> bool:
        """เช็คว่าดูการจองทั้งหมดได้ไหม"""
        return self.role == UserRole.ADMIN.value

    def can_view_all_users(self) -> bool:
        """เช็คว่าดู Users ทั้งหมดได้ไหม"""
        return self.role == UserRole.ADMIN.value

    # ════════════════════════════════════════════════════════════════
    # METHODS - Utility
    # ════════════════════════════════════════════════════════════════
    def get_full_name(self) -> str:
        """ดึงชื่อเต็ม"""
        return f"{self.first_name} {self.last_name}"

    def get_display_name(self) -> str:
        """ดึงชื่อแสดงผล (ชื่อ + role)"""
        role_display = {
            UserRole.ADMIN.value: "ผู้ดูแลระบบ",
            UserRole.TEACHER.value: "อาจารย์",
            UserRole.STUDENT.value: "นักศึกษา"
        }
        return f"{self.get_full_name()} ({role_display.get(self.role, self.role)})"
    

# dummy
# const Profiles = [
#     {
#     id: user1,
#     auth_user_id: auth0|123,
#     first_name: 'Wichayaporn',
#     last_name: 'Srisawat',
#     role: 'admin'
#     },
#     {
#     id: user2,
#     auth_user_id: auth0|456,
#     first_name: 'John',
#     last_name: 'Doe', 
#     role: 'teacher'
#     },
#     {
#     id: user3,
#     auth_user_id: auth0|789,      
#     first_name: 'Jane',
#     last_name: 'Smith',
#     role: 'student'
#     }]    