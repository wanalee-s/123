from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

# CREATE SCHEMA - ใช้ตอนเพิ่มอุปกรณ์ในห้อง
class RoomEquipmentCreate(BaseModel):
    room_id: UUID
    equipment_id: UUID
    quantity: int = Field(default=1, ge=1)

# UPDATE SCHEMA - ใช้ตอนแก้ไขจำนวน
class RoomEquipmentUpdate(BaseModel):
    quantity: int = Field(..., ge=1)

# RESPONSE SCHEMA - ใช้ตอบกลับ (ข้อมูลพื้นฐาน)
class RoomEquipmentResponse(BaseModel):
    id: UUID
    room_id: UUID
    equipment_id: UUID
    quantity: int
    created_at: datetime
    created_by: Optional[UUID] = None

    class Config:
        from_attributes = True

# ADJUST SCHEMA - ใช้ตอนปรับจำนวน (+/-)
class RoomEquipmentAdjust(BaseModel):
    amount: int = Field(..., description="จำนวนที่จะปรับ (+ เพิ่ม, - ลด)")


# DETAILED RESPONSE - ใช้ตอบกลับ (พร้อมชื่อห้องและอุปกรณ์)
class RoomEquipmentDetail(RoomEquipmentResponse):
    room_name: Optional[str] = None
    equipment_name: Optional[str] = None