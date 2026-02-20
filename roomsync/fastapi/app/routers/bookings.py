'''
ความสัมพันธ์:
┌──────────┐         ┌───────────────┐         ┌─────────────┐
│   User   │ ──────► │    Booking    │ ◄────── │    Room     │
│ (ผู้จอง)  │         │   (การจอง)    │         │   (ห้อง)    │
│Supabase  │         └───────────────┘         └─────────────┘
└──────────┘                │
                            │
                    ┌───────┴───────┐
                    │    Status     │
                    ├───────────────┤
                    │ • pending     │ รออนุมัติ
                    │ • approved    │ อนุมัติแล้ว
                    │ • rejected    │ ถูกปฏิเสธ
                    │ • cancelled   │ ยกเลิกแล้ว
                    └───────────────┘
สถานะของ Booking:
                                    ┌───────────┐
                              ┌───► │ APPROVED  │ ───► ใช้ห้องได้
                              │     │ (อนุมัติ)  │
                              │     └───────────┘
┌──────────┐    Admin         │
│ PENDING  │ ─────────────────┤
│ (รออนุมัติ)│    ตัดสินใจ       │     ┌───────────┐
└──────────┘                  └───► │ REJECTED  │ ───► ใช้ห้องไม่ได้
      │                             │ (ปฏิเสธ)   │
      │                             └───────────┘
      │         User ยกเลิกเอง
      └─────────────────────────────┐
                                    ▼
                              ┌───────────┐
                              │ CANCELLED │ ───► ยกเลิกแล้ว
                              │ (ยกเลิก)   │
                              └───────────┘
'''



from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from uuid import UUID

from app.db import get_db
from app.models.booking import Booking, BookingStatus
from app.models.room import Room
from app.schemas.booking import BookingCreate, BookingUpdate, BookingResponse

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("/", response_model=List[BookingResponse])
def get_all_bookings(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    room_id: Optional[UUID] = None,
    user_id: Optional[UUID] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Booking)
    if status:
        query = query.filter(Booking.status == status)
    if room_id:
        query = query.filter(Booking.room_id == room_id)
    if user_id:
        query = query.filter(Booking.user_id == user_id)
    return query.order_by(Booking.start_time.desc()).offset(skip).limit(limit).all()


@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(booking_id: UUID, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(
    booking_data: BookingCreate,
    user_id: UUID = Query(..., description="User ID from Supabase Auth"),
    db: Session = Depends(get_db)
):
    room = db.query(Room).filter(Room.id == booking_data.room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    if not room.status:
        raise HTTPException(status_code=400, detail="Room is not available")
    
    # Check conflicts
    conflict = db.query(Booking).filter(
        Booking.room_id == booking_data.room_id,
        Booking.status.in_([BookingStatus.PENDING.value, BookingStatus.APPROVED.value]),
        or_(
            and_(Booking.start_time <= booking_data.start_time, Booking.end_time > booking_data.start_time),
            and_(Booking.start_time < booking_data.end_time, Booking.end_time >= booking_data.end_time),
            and_(Booking.start_time >= booking_data.start_time, Booking.end_time <= booking_data.end_time)
        )
    ).first()
    
    if conflict:
        raise HTTPException(status_code=400, detail="Room is already booked for this time slot")
    
    booking = Booking(
        user_id=user_id,
        room_id=booking_data.room_id,
        start_time=booking_data.start_time,
        end_time=booking_data.end_time,
        status=BookingStatus.PENDING.value,
        created_by=user_id
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


@router.patch("/{booking_id}/approve", response_model=BookingResponse)
def approve_booking(booking_id: UUID, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.status != BookingStatus.PENDING.value:
        raise HTTPException(status_code=400, detail="Booking is not pending")
    booking.status = BookingStatus.APPROVED.value
    db.commit()
    db.refresh(booking)
    return booking


@router.patch("/{booking_id}/reject", response_model=BookingResponse)
def reject_booking(booking_id: UUID, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    booking.status = BookingStatus.REJECTED.value
    db.commit()
    db.refresh(booking)
    return booking


@router.patch("/{booking_id}/cancel", response_model=BookingResponse)
def cancel_booking(booking_id: UUID, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    booking.status = BookingStatus.CANCELLED.value
    db.commit()
    db.refresh(booking)
    return booking


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(booking_id: UUID, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(booking)
    db.commit()