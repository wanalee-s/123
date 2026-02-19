from sqlalchemy import Column, Integer, Boolean, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db import Base


class Room(Base):
    """Model สำหรับตาราง rooms"""
    __tablename__ = "rooms"

    # PRIMARY KEY
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # ROOM INFO
    name = Column(Text, nullable=False)
    capacity = Column(Integer, default=1)
    status = Column(Boolean, default=True)
    
    # TIMESTAMPS
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    # AUDIT FIELDS   
    created_by = Column(UUID(as_uuid=True), nullable=True)
    updated_by = Column(UUID(as_uuid=True), nullable=True)
    
    # RELATIONSHIPS
    bookings = relationship("Booking", back_populates="room", cascade="all, delete-orphan")
    room_equipments = relationship("RoomEquipment", back_populates="room", cascade="all, delete-orphan")
    damage_reports = relationship("DamageReport", back_populates="room", cascade="all, delete-orphan")


    # ════════════════════════════════════════════════════════════════
    # METHODS
    # ════════════════════════════════════════════════════════════════
    def __repr__(self):
        return f"<Room {self.name} (capacity={self.capacity}, status={self.status})>"
    
    def is_available(self) -> bool:
        """เช็คว่าห้องพร้อมใช้งานไหม"""
        return self.status == True
    
    def get_equipment_count(self) -> int:
        """นับจำนวนประเภทอุปกรณ์ในห้อง"""
        return len(self.room_equipments)
    
    def get_total_equipment_quantity(self) -> int:
        """นับจำนวนอุปกรณ์ทั้งหมดในห้อง"""
        return sum(re.quantity for re in self.room_equipments)