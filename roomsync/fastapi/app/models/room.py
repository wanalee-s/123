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
    pax = Column(Integer, default=1)
    level = Column(Text, nullable=False)
    status = Column(Text, nullable=False)
    note = Column(Text, nullable=True)
    image_path = Column(str(255), nullable=True)
    
    # TIMESTAMPS ROOM
    until = Column(DateTime(timezone=True))
    activeTime = Column(DateTime(timezone=True))

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
        return f"<Room {self.name} (pax={self.pax}, status={self.status})>"
    
    def is_available(self) -> bool:
        """เช็คว่าห้องพร้อมใช้งานไหม"""
        return self.status == 'available'
    
    def get_equipment_count(self) -> int:
        """นับจำนวนประเภทอุปกรณ์ในห้อง"""
        return len(self.room_equipments)
    
    def get_total_equipment_quantity(self) -> int:
        """นับจำนวนอุปกรณ์ทั้งหมดในห้อง"""
        return sum(re.quantity for re in self.room_equipments)
    

    #dummy
#     image_path is picture path in your computer
#     const rooms = [
#     {
#         id: room1,
#         name: 'CSB100',
#         level: 'Level 1, East',
#         until: '4:00 PM',
#         activeTime: '2h 30m',
#         note: null,
#         pax: 12,
#         status: 'available',
#         image_path: '/uploads/roomPic_01.webp'
#     },
#     {
#         id: room2,
#         name: 'CSB201',
#         level: 'Level 2, West',
#         until: '4:30 PM',
#         activeTime: '1h 12m',
#         note: null,
#         pax: 8,
#         status: 'booked',
#         image_path: '/uploads/roomPic_02.webp'
#     },
#     {
#         id: room3,
#         name: 'CSB301',
#         level: 'Level 3, East',
#         until: null,
#         activeTime: '3h 45m',
#         note: 'tempurature so cold',
#         pax: 20,
#         status: 'inuse',
#         image_path: '/uploads/roomPic_03.webp'
#     },
#     {
#         id: room4,
#         name: 'CSB307',
#         level: 'Level 3, West',
#         until: null,
#         activeTime: null,
#         note: 'Under Repair',
#         pax: 1,
#         status: 'broken',
#         image_path: '/uploads/roomPic_04.webp'
#     },
#     {
#         id: room5,
#         name: 'CSB308',
#         level: 'Level 3, West',
#         until: null,
#         activeTime: null,
#         note: 'Under Repair',
#         pax: 1,
#         status: 'broken',
#         image_path: '/uploads/roomPic_05.webp'
#     }
# ]
