from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db import get_db
from app.models.room import Room
from app.models.room_equipment import RoomEquipment
from app.models.equipment import Equipment
from app.schemas.room import RoomCreate, RoomUpdate, RoomResponse, RoomWithEquipments, EquipmentInRoom

# สร้าง Router
router = APIRouter(prefix="/rooms", tags=["Rooms"])
# เมื่อ main.py ใช้: app.include_router(rooms.router, prefix="/api/v1")
# URL จริงจะเป็น: /api/v1/rooms/...

# GET - ดึงห้องทั้งหมด
@router.get("/", response_model=List[RoomResponse])
def get_all_rooms(
    skip: int = 0,       # ข้ามกี่ record (pagination)
    limit: int = 100,    # เอากี่ record
    status: bool = None, # filter ตาม status
    db: Session = Depends(get_db) # inject database session ยืมมาใช้ก่อนน้า
):
    query = db.query(Room) # SELECT * FROM rooms

    # ถ้ามี filter status
    if status is not None:
        query = query.filter(Room.status == status) # WHERE status = ?
    return query.offset(skip).limit(limit).all()    # OFFSET ? LIMIT ?

#  GET - ดึงห้องตาม ID
@router.get("/{room_id}", response_model=RoomWithEquipments)
def get_room(room_id: UUID, db: Session = Depends(get_db)):
    # 1. หาห้องจาก ID
    room = db.query(Room).filter(Room.id == room_id).first()

     # 2. ถ้าไม่เจอ → Error 404
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
     # 3. ดึง equipments ในห้องนี้ (JOIN query)
    room_equipments = db.query(
        Equipment.id, Equipment.name, RoomEquipment.quantity
    ).join(RoomEquipment).filter(RoomEquipment.room_id == room_id).all()
    
    # 4. แปลงเป็น list ของ EquipmentInRoom
    equipments = [
        EquipmentInRoom(id=eq.id, name=eq.name, quantity=eq.quantity)
        for eq in room_equipments
    ]
    
    # 5. รวม room + equipments แล้ว return
    return RoomWithEquipments(
        **RoomResponse.model_validate(room).model_dump(),
        equipments=equipments
    )

# POST - สร้างห้องใหม่
@router.post("/", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create_room(room_data: RoomCreate, db: Session = Depends(get_db)):
    # 1. สร้าง Room object จากข้อมูลที่ส่งมา
    room = Room(**room_data.model_dump()) # เท่ากับ: Room(name="ห้อง A", capacity=10, status=True)
    db.add(room)         # 2. เพิ่มลง database
    db.commit()          # 3. บันทึก
    db.refresh(room)     # 4. refresh เพื่อดึง id ที่ database generate มา
    return room          # 5. return ห้องที่สร้าง

#  PUT - อัพเดทห้อง
@router.put("/{room_id}", response_model=RoomResponse)
def update_room(room_id: UUID, room_data: RoomUpdate, db: Session = Depends(get_db)):
    # 1. หาห้องที่จะอัพเดท
    room = db.query(Room).filter(Room.id == room_id).first()

     # 2. ไม่เจอ → Error 404
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    # 3. อัพเดทเฉพาะ field ที่ส่งมา
    for field, value in room_data.model_dump(exclude_unset=True).items():
        setattr(room, field, value)
    # exclude_unset=True → ไม่รวม field ที่ไม่ได้ส่งมา
    
    db.commit()
    db.refresh(room)
    return room

# DELETE - ลบห้อง
@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(room_id: UUID, db: Session = Depends(get_db)):
    # 1. หาห้อง
    room = db.query(Room).filter(Room.id == room_id).first()
    # 2. ไม่เจอ → Error 404
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    db.delete(room) # 3. ลบ
    db.commit()
    # 4. ไม่ return อะไร (204 No Content  สำเร็จ แต่ไม่มี response body)

#  GET - ดึงเฉพาะห้องว่าง
@router.get("/available/", response_model=List[RoomResponse])
def get_available_rooms(db: Session = Depends(get_db)):
    return db.query(Room).filter(Room.status == True).all()