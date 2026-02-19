from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime
from enum import Enum

# ENUM - สถานะของรายงาน
class DamageStatusEnum(str, Enum):
    REPORTED = "reported"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"

# BASE SCHEMA - ใช้เป็นฐาน
class DamageReportBase(BaseModel):
    room_id: UUID
    equipment_id: Optional[UUID] = None
    description: str = Field(..., min_length=1)

# CREATE SCHEMA - ใช้ตอนแจ้งซ่อม
class DamageReportCreate(DamageReportBase):
    pass

# UPDATE SCHEMA - ใช้ตอนแก้ไขรายงาน
class DamageReportUpdate(BaseModel):
    description: Optional[str] = Field(None, min_length=1)
    status: Optional[DamageStatusEnum] = None

# RESPONSE SCHEMA - ใช้ตอบกลับ (พื้นฐาน)
class DamageReportResponse(DamageReportBase):
    id: UUID
    reporter_id: UUID
    status: str
    created_at: datetime
    updated_at: datetime
    created_by: Optional[UUID] = None
    updated_by: Optional[UUID] = None

    class Config:
        from_attributes = True

# ════════════════════════════════════════════════════════════════════════════
# STATUS UPDATE SCHEMA - ใช้ตอนเปลี่ยนสถานะอย่างเดียว
# ════════════════════════════════════════════════════════════════════════════
class DamageReportStatusUpdate(BaseModel):
    status: DamageStatusEnum