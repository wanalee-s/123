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
#     room_id: "room1", 509930fd-3ff5-45e6-8a6a-2b6a392cbebe
#     equipment_id: "eq-1", 132132cc-4a22-4b3b-84d5-e5f43b3a962b
#     quantity: 2
#     },
#     {
#     id: "re-2",
#     room_id: "room1", bc7bf963-8c0f-4131-8564-74fa4b452c50
#     equipment_id: "eq-2", d5f44b63-c6d4-4ea2-a64b-5f2415dc2aac
#     quantity: 1
#     },
#     {
#     id: "re-3",
#     room_id: "room2", e2751ad6-ad9f-422f-856d-8638a8ac2bc7
#     equipment_id: "eq-1", e7ce4917-1294-4873-bf27-5632bc9dc090
#     quantity: 1
#     }]