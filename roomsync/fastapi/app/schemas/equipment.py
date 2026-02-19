from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

# BASE SCHEMA - ใช้เป็นฐาน
class EquipmentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None

# CREATE SCHEMA - ใช้ตอนสร้างอุปกรณ์ใหม่
class EquipmentCreate(EquipmentBase):
    pass

# UPDATE SCHEMA - ใช้ตอนแก้ไขอุปกรณ์
class EquipmentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None

# RESPONSE SCHEMA - ใช้ตอบกลับ (พื้นฐาน)
class EquipmentResponse(EquipmentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    created_by: Optional[UUID] = None
    updated_by: Optional[UUID] = None

    class Config:
        from_attributes = True

# ════════════════════════════════════════════════════════════════════════════
# NESTED SCHEMA - ใช้แสดงห้องที่มีอุปกรณ์นี้
# ════════════════════════════════════════════════════════════════════════════
class RoomWithQuantity(BaseModel):
    room_id: UUID
    room_name: str
    quantity: int

    class Config:
        from_attributes = True
# ════════════════════════════════════════════════════════════════════════════
# EXTENDED RESPONSE - อุปกรณ์พร้อมรายการห้องที่มี
# ════════════════════════════════════════════════════════════════════════════
class EquipmentWithRooms(EquipmentResponse):
    rooms: List[RoomWithQuantity] = []
    total_quantity: int = 0


# ════════════════════════════════════════════════════════════════════════════
# SUMMARY SCHEMA - สรุปจำนวนอุปกรณ์ (สำหรับ Dashboard)
# ════════════════════════════════════════════════════════════════════════════
class EquipmentSummary(BaseModel):
    id: UUID
    name: str
    total_quantity: int
    rooms_count: int

    class Config:
        from_attributes = True