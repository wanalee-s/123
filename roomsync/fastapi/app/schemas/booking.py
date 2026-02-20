from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional
from uuid import UUID
from datetime import datetime
from enum import Enum

# ENUM - สถานะของการจอง
class BookingStatusEnum(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"

# BASE SCHEMA - ใช้เป็นฐาน
class BookingBase(BaseModel):
    room_id: UUID
    start_time: datetime
    end_time: datetime

    @field_validator('end_time')
    @classmethod
    def end_time_must_be_after_start_time(cls, v, info):
        """ตรวจสอบว่า end_time ต้องมาหลัง start_time"""
        if 'start_time' in info.data and v <= info.data['start_time']:
            raise ValueError('end_time must be after start_time')
        return v
    @model_validator(mode='after')
    def validate_booking_duration(self):
        """ตรวจสอบระยะเวลาการจอง"""
        if hasattr(self, 'start_time') and hasattr(self, 'end_time') and self.start_time and self.end_time:
            duration = (self.end_time - self.start_time).total_seconds() / 3600
            
            # ต้องจองอย่างน้อย 30 นาที
            if duration < 0.5:
                raise ValueError('Booking must be at least 30 minutes')
            
            # จองได้สูงสุด 8 ชั่วโมง
            if duration > 8:
                raise ValueError('Booking cannot exceed 8 hours')
        
        return self

# CREATE SCHEMA - ใช้ตอนจองห้อง
class BookingCreate(BookingBase):
    pass

# STATUS UPDATE SCHEMA - ใช้ตอนเปลี่ยนสถานะ
class BookingUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[BookingStatusEnum] = None

# RESPONSE SCHEMA - ใช้ตอบกลับ (พื้นฐาน)
class BookingResponse(BookingBase):
    id: UUID
    user_id: UUID
    status: str
    created_at: datetime
    updated_at: datetime
    created_by: Optional[UUID] = None
    updated_by: Optional[UUID] = None

    class Config:
        from_attributes = True



# ════════════════════════════════════════════════════════════════════════════
# CALENDAR VIEW - สำหรับแสดงปฏิทิน
# ════════════════════════════════════════════════════════════════════════════
class BookingCalendarItem(BaseModel):
    id: UUID
    title: Optional[str] = None
    room_id: UUID
    room_name: str
    start_time: datetime
    end_time: datetime
    status: str
    booker_name: str

    class Config:
        from_attributes = True