from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime, time

# BASE SCHEMA - ใช้เป็นฐานสำหรับ Schema อื่น
class RoomBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    pax: int = Field(default=1, ge=1)
    level: int = Field(..., description="Floor level")
    status: str = Field(..., description="Room status: available, booked, inuse, broken, etc.")
    note: Optional[str] = None
    image_path: Optional[str] = Field(None, max_length=255)

    until: Optional[datetime] = None
    activeTime: Optional[time] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[UUID] = None
    updated_by: Optional[UUID] = None

# CREATE SCHEMA - ใช้ตอนสร้างห้องใหม่
class RoomCreate(RoomBase):
    pass

# UPDATE SCHEMA - ใช้ตอนอัพเดทห้อง
class RoomUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    pax: Optional[int] = Field(None, ge=1)
    level: Optional[int] = None
    status: Optional[str] = None
    note: Optional[str] = None
    image_path: Optional[str] = Field(None, max_length=255)

# RESPONSE SCHEMA - ใช้ตอบกลับ
class RoomResponse(RoomBase):
    id: UUID
    until: Optional[datetime] = None
    activeTime: Optional[time] = None
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