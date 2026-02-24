from sqlalchemy import Column, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db import Base


class Equipment(Base):
    __tablename__ = "equipments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), nullable=True)
    updated_by = Column(UUID(as_uuid=True), nullable=True)
    
    room_equipments = relationship("RoomEquipment", back_populates="equipment", cascade="all, delete-orphan")
    damage_reports = relationship("DamageReport", back_populates="equipment")

# dummy
# const Equipments = [
#     {
#     id: eq-1,
#     name: 'Projector',
#     description: 'Epson X1234, 4000 lumens'
#     },
#     {
#     id: eq-2,
#     name: 'Whiteboard',
#     description: '120x90 cm, with markers'
#     },
#     {
#     id: eq-3,
#     name: 'Conference Phone',
#     description: 'Polycom SoundStation IP 6000'
#     }]
