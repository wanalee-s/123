from sqlalchemy import Column, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from app.db import Base


# ════════════════════════════════════════════════════════════════
# ENUM - สถานะของการจอง
# ════════════════════════════════════════════════════════════════
class BookingStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


# ════════════════════════════════════════════════════════════════
# BOOKING MODEL
# ════════════════════════════════════════════════════════════════
class Booking(Base):
    """Model สำหรับตาราง bookings"""

    __tablename__ = "bookings"

    # ════════════════════════════════════════════════════════════════
    # PRIMARY KEY
    # ════════════════════════════════════════════════════════════════
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # ════════════════════════════════════════════════════════════════
    # FOREIGN KEYS
    # ════════════════════════════════════════════════════════════════
    user_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    room_id = Column(UUID(as_uuid=True), ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)

    # ════════════════════════════════════════════════════════════════
    # BOOKING DETAILS
    # ════════════════════════════════════════════════════════════════
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(Text, default=BookingStatus.PENDING.value, nullable=False)

    # ════════════════════════════════════════════════════════════════
    # TIMESTAMPS
    # ════════════════════════════════════════════════════════════════
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    # ════════════════════════════════════════════════════════════════
    # AUDIT FIELDS
    # ════════════════════════════════════════════════════════════════
    created_by = Column(UUID(as_uuid=True), nullable=True)
    updated_by = Column(UUID(as_uuid=True), nullable=True)

    # ════════════════════════════════════════════════════════════════
    # RELATIONSHIPS
    # ════════════════════════════════════════════════════════════════
    # Many-to-One: Booking belongs to a Room
    room = relationship("Room", back_populates="bookings")

    # Many-to-One: Booking belongs to a Profile (user)
    profile = relationship("Profile", back_populates="bookings")

    # ════════════════════════════════════════════════════════════════
    # METHODS
    # ════════════════════════════════════════════════════════════════
    def __repr__(self):
        return f"<Booking {self.id} - Room: {self.room_id}, User: {self.user_id}, Status: {self.status}>"

    def is_pending(self) -> bool:
        """เช็คว่าการจองยังรอการอนุมัติไหม"""
        return self.status == BookingStatus.PENDING.value

    def is_approved(self) -> bool:
        """เช็คว่าการจองได้รับการอนุมัติแล้วไหม"""
        return self.status == BookingStatus.APPROVED.value

    def is_rejected(self) -> bool:
        """เช็คว่าการจองถูกปฏิเสธไหม"""
        return self.status == BookingStatus.REJECTED.value

    def is_cancelled(self) -> bool:
        """เช็คว่าการจองถูกยกเลิกไหม"""
        return self.status == BookingStatus.CANCELLED.value

    def can_be_modified(self) -> bool:
        """เช็คว่าการจองสามารถแก้ไขได้ไหม (เฉพาะสถานะ pending)"""
        return self.status == BookingStatus.PENDING.value

    def get_duration_hours(self) -> float:
        """คำนวณระยะเวลาการจองเป็นชั่วโมง"""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds() / 3600
        return 0.0

    def overlaps_with(self, other_booking) -> bool:
        """เช็คว่าการจองนี้ทับซ้อนกับการจองอื่นไหม"""
        return (
            self.room_id == other_booking.room_id and
            self.id != other_booking.id and  # ไม่ใช่ตัวเอง
            self.start_time < other_booking.end_time and
            self.end_time > other_booking.start_time
        )


# dummy 
# const Bookings = [
#     { 
#     id: booking1,
#     user_id: user1,   
#     room_id: room1,
#     start_time: '2024-10-01T09:00:00',
#     end_time: '2024-10-01T11:00:00',
#     status: 'approved'
#     },
#     {
#     id: booking2,
#     user_id: user2,
#     room_id: room1,
#     start_time: '2024-10-01T12:00:00',
#     end_time: '2024-10-01T14:00:00',
#     status: 'pending'
#     },
#     {
#     id: booking3,
#     user_id: user3,
#     room_id: room2,
#     start_time: '2024-10-01T10:00:00',
#     end_time: '2024-10-01T12:00:00',
#     status: 'rejected'
#     }]