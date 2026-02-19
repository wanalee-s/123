from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db import get_db
from app.models.room_equipment import RoomEquipment
from app.models.room import Room
from app.models.equipment import Equipment
from app.schemas.room_equipment import RoomEquipmentCreate, RoomEquipmentUpdate, RoomEquipmentResponse

router = APIRouter(prefix="/room-equipments", tags=["Room Equipments"])


# ──────────────────────────────────────────────────────────────────
# GET - ดึงอุปกรณ์ทั้งหมดในห้อง
# ──────────────────────────────────────────────────────────────────
@router.get("/room/{room_id}", response_model=List[RoomEquipmentResponse])
def get_equipments_in_room(room_id: UUID, db: Session = Depends(get_db)):
    """ดึงรายการอุปกรณ์ทั้งหมดในห้อง"""
    return db.query(RoomEquipment).filter(RoomEquipment.room_id == room_id).all()


# ──────────────────────────────────────────────────────────────────
# POST - เพิ่มอุปกรณ์ในห้อง (ถ้ามีอยู่แล้วจะเพิ่มจำนวน)
# ──────────────────────────────────────────────────────────────────
@router.post("/", response_model=RoomEquipmentResponse, status_code=status.HTTP_201_CREATED)
def add_equipment_to_room(data: RoomEquipmentCreate, db: Session = Depends(get_db)):
    """เพิ่มอุปกรณ์ในห้อง (ถ้ามีอยู่แล้วจะเพิ่มจำนวน)"""
    
    # ตรวจสอบว่าห้องมีจริง
    if not db.query(Room).filter(Room.id == data.room_id).first():
        raise HTTPException(status_code=404, detail="Room not found")
    
    # ตรวจสอบว่าอุปกรณ์มีจริง
    if not db.query(Equipment).filter(Equipment.id == data.equipment_id).first():
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    # ตรวจสอบว่ามีอยู่แล้วหรือยัง
    existing = db.query(RoomEquipment).filter(
        RoomEquipment.room_id == data.room_id,
        RoomEquipment.equipment_id == data.equipment_id
    ).first()
    
    # ถ้ามีอยู่แล้ว → เพิ่มจำนวน
    if existing:
        existing.quantity += data.quantity
        db.commit()
        db.refresh(existing)
        return existing
    
    # ถ้ายังไม่มี → สร้างใหม่
    room_equipment = RoomEquipment(**data.model_dump())
    db.add(room_equipment)
    db.commit()
    db.refresh(room_equipment)
    return room_equipment


# ──────────────────────────────────────────────────────────────────
# PUT - Set จำนวนอุปกรณ์ใหม่ (แทนที่ค่าเดิม)
# ──────────────────────────────────────────────────────────────────
@router.put("/{id}", response_model=RoomEquipmentResponse)
def update_room_equipment(id: UUID, data: RoomEquipmentUpdate, db: Session = Depends(get_db)):
    """Set จำนวนอุปกรณ์ใหม่ (แทนที่ค่าเดิม)"""
    
    room_equipment = db.query(RoomEquipment).filter(RoomEquipment.id == id).first()
    
    if not room_equipment:
        raise HTTPException(status_code=404, detail="Room equipment not found")
    
    room_equipment.quantity = data.quantity
    db.commit()
    db.refresh(room_equipment)
    return room_equipment


# ──────────────────────────────────────────────────────────────────
# PATCH - ปรับจำนวนอุปกรณ์ (+เพิ่ม หรือ -ลด)  ⭐ NEW
# ──────────────────────────────────────────────────────────────────
@router.patch("/{id}/adjust", response_model=RoomEquipmentResponse)
def adjust_equipment_quantity(
    id: UUID,
    amount: int = Query(..., description="จำนวนที่จะปรับ (+ เพิ่ม, - ลด)"),
    db: Session = Depends(get_db)
):
    """
    ปรับจำนวนอุปกรณ์ในห้อง
    - amount เป็นบวก (+) = เพิ่มจำนวน
    - amount เป็นลบ (-) = ลดจำนวน
    - ถ้าเหลือ 0 จะลบ record ออกอัตโนมัติ
    """
    
    room_equipment = db.query(RoomEquipment).filter(RoomEquipment.id == id).first()
    
    if not room_equipment:
        raise HTTPException(status_code=404, detail="Room equipment not found")
    
    # คำนวณจำนวนใหม่
    new_quantity = room_equipment.quantity + amount
    
    # ตรวจสอบว่าไม่ติดลบ
    if new_quantity < 0:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot reduce by {abs(amount)}. Only {room_equipment.quantity} available"
        )
    
    # ถ้าเหลือ 0 → ลบ record ทิ้ง
    if new_quantity == 0:
        db.delete(room_equipment)
        db.commit()
        # Return response ก่อนลบ พร้อมบอกว่าถูกลบแล้ว
        raise HTTPException(
            status_code=200,
            detail=f"Equipment removed from room (quantity reached 0)"
        )
    
    # อัพเดทจำนวน
    room_equipment.quantity = new_quantity
    db.commit()
    db.refresh(room_equipment)
    return room_equipment


# ──────────────────────────────────────────────────────────────────
# DELETE - ลบอุปกรณ์ออกจากห้องทั้งหมด
# ──────────────────────────────────────────────────────────────────
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_equipment_from_room(id: UUID, db: Session = Depends(get_db)):
    """ลบอุปกรณ์ออกจากห้องทั้งหมด"""
    
    room_equipment = db.query(RoomEquipment).filter(RoomEquipment.id == id).first()
    
    if not room_equipment:
        raise HTTPException(status_code=404, detail="Room equipment not found")
    
    db.delete(room_equipment)
    db.commit()