from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime

# BASE SCHEMA - ใช้เป็นฐานสำหรับ Schema อื่น
class RoomBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    capacity: int = Field(default=1, ge=1)
    status: bool = Field(default=True)

# CREATE SCHEMA - ใช้ตอนสร้างห้องใหม่
class RoomCreate(RoomBase):
    pass

# UPDATE SCHEMA - ใช้ตอนอัพเดทห้อง
class RoomUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    capacity: Optional[int] = Field(None, ge=1)
    status: Optional[bool] = None

# RESPONSE SCHEMA - ใช้ตอบกลับ
class RoomResponse(RoomBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    created_by: Optional[UUID] = None
    updated_by: Optional[UUID] = None

    class Config:
        from_attributes = True

# NESTED SCHEMA - ใช้สำหรับแสดง Equipment ในห้อง
class EquipmentInRoom(BaseModel):
    id: UUID
    name: str
    quantity: int

    class Config:
        from_attributes = True

# EXTENDED RESPONSE - Room พร้อม Equipments
class RoomWithEquipments(RoomResponse):
    equipments: List[EquipmentInRoom] = []