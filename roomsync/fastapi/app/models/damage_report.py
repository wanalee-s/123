from sqlalchemy import Column, DateTime, Text, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from app.db import Base


class DamageStatus(str, enum.Enum):
    REPORTED = "reported"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"


class DamageReport(Base):
    __tablename__ = "damage_reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    room_id = Column(UUID(as_uuid=True), ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)
    equipment_id = Column(UUID(as_uuid=True), ForeignKey("equipments.id", ondelete="SET NULL"), nullable=True)
    reporter_id = Column(UUID(as_uuid=True), nullable=False)
    
    description = Column(Text, nullable=False)
    status = Column(String(20), default=DamageStatus.REPORTED.value)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), nullable=True)
    updated_by = Column(UUID(as_uuid=True), nullable=True)
    
    room = relationship("Room", back_populates="damage_reports")
    equipment = relationship("Equipment", back_populates="damage_reports")

# dummy
# const DamageReports = [
#     {
#     id: dr-1,
#     room_id: room1,
#     equipment_id: eq-1,
#     reporter_id: user1,
#     description: 'Projector bulb is broken',
#     status: 'reported'
#     },
#     {
#     id: dr-2,
#     room_id: room2,
#     equipment_id: eq-2,
#     reporter_id: user2,
#     description: 'Whiteboard markers are missing',
#     status: 'in_progress'
#     },
#     {
#     id: dr-3,
#     room_id: room3,
#     equipment_id: eq-1,
#     reporter_id: user3,
#     description: 'Projector bulb is broken',
#     status: 'resolved'
#    }]   