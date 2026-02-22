from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db import Base


class RoomEquipment(Base):
    __tablename__ = "room_equipments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    room_id = Column(UUID(as_uuid=True), ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)
    equipment_id = Column(UUID(as_uuid=True), ForeignKey("equipments.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, default=1)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), nullable=True)
    
    room = relationship("Room", back_populates="room_equipments")
    equipment = relationship("Equipment", back_populates="room_equipments")


# dummy
# const RoomEquipments = [
#     {
#     id: "re-1",
#     room_id: "room1",
#     equipment_id: "eq-1",
#     quantity: 2
#     },
#     {
#     id: "re-2",
#     room_id: "room1",
#     equipment_id: "eq-2",
#     quantity: 1
#     },
#     {
#     id: "re-3",
#     room_id: "room2",
#     equipment_id: "eq-1",
#     quantity: 1
#     }]