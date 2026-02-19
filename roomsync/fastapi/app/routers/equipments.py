# Equipment (อุปกรณ์มีอะไรบ้าง)
#      │
#      ▼
# RoomEquipment (อุปกรณ์ไหนอยู่ห้องไหน จำนวนเท่าไหร่)
#      │
#      ▼
# Room (ห้อง)


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db import get_db
from app.models.equipment import Equipment
from app.schemas.equipment import EquipmentCreate, EquipmentUpdate, EquipmentResponse

# สร้าง Router
router = APIRouter(prefix="/equipments", tags=["Equipments"])

# GET - ดึงอุปกรณ์ทั้งหมด
@router.get("/", response_model=List[EquipmentResponse])
def get_all_equipments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Equipment).offset(skip).limit(limit).all()

# GET - ดึงอุปกรณ์ตาม ID
@router.get("/{equipment_id}", response_model=EquipmentResponse)
def get_equipment(equipment_id: UUID, db: Session = Depends(get_db)):
    # 1. หาอุปกรณ์จาก ID
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    # 2. ไม่เจอ → Error 404
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    # 3. Return อุปกรณ์
    return equipment

#  POST - สร้างอุปกรณ์ใหม่
@router.post("/", response_model=EquipmentResponse, status_code=status.HTTP_201_CREATED)
def create_equipment(equipment_data: EquipmentCreate, db: Session = Depends(get_db)):
    # 1. สร้าง Equipment object
    equipment = Equipment(**equipment_data.model_dump())
    # เท่ากับ: Equipment(name="โปรเจคเตอร์", description="Epson...")

    # 2. เพิ่มลง database
    db.add(equipment)
    db.commit()
    db.refresh(equipment)
    return equipment

# PUT - อัพเดทอุปกรณ์
@router.put("/{equipment_id}", response_model=EquipmentResponse)
def update_equipment(equipment_id: UUID, equipment_data: EquipmentUpdate, db: Session = Depends(get_db)):
    # 1. หาอุปกรณ์
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    # 2. ไม่เจอ → 404
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    # 3. อัพเดทเฉพาะ field ที่ส่งมา
    for field, value in equipment_data.model_dump(exclude_unset=True).items():
        setattr(equipment, field, value)
    # 4. บันทึก
    db.commit()
    db.refresh(equipment)
    return equipment

# DELETE - ลบอุปกรณ์
@router.delete("/{equipment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_equipment(equipment_id: UUID, db: Session = Depends(get_db)):
    # 1. หาอุปกรณ์
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    # 2. ไม่เจอ → 404
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    # 3. ลบ
    db.delete(equipment)
    db.commit()