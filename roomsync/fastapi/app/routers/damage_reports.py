'''
ความสัมพันธ์:
┌──────────┐         ┌───────────────┐         ┌─────────────┐
│   Room   │ ◄────── │ DamageReport  │ ──────► │  Equipment  │
│  (ห้อง)  │         │ (รายงาน)       │         │  (อุปกรณ์)   │
└──────────┘         └───────────────┘         └─────────────┘
                            │
                            ▼
                     ┌─────────────┐
                     │    User     │
                     │ (ผู้รายงาน)  │
                     │ Supabase Auth│
                     └─────────────┘
สถานะของ Report:
┌──────────┐      ┌─────────────┐      ┌──────────┐
│ REPORTED │ ───► │ IN_PROGRESS │ ───► │ RESOLVED │
│ (แจ้งแล้ว) │      │ (กำลังซ่อม)   │      │ (เสร็จแล้ว) │
└──────────┘      └─────────────┘      └──────────┘
'''



from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.db import get_db
from app.models.damage_report import DamageReport, DamageStatus
from app.models.room import Room
from app.schemas.damage_report import DamageReportCreate, DamageReportUpdate, DamageReportResponse

#  สร้าง Router
router = APIRouter(prefix="/damage-reports", tags=["Damage Reports"])

# GET - ดึงรายงานทั้งหมด (พร้อม Filter)
@router.get("/", response_model=List[DamageReportResponse])
def get_all_damage_reports(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    room_id: Optional[UUID] = None,
    db: Session = Depends(get_db)
):
    """ดึงรายงานความเสียหายทั้งหมด"""
    # เริ่มจาก query ทั้งหมด
    query = db.query(DamageReport)

    # ถ้ามี filter status
    if status:
        query = query.filter(DamageReport.status == status) #ซ่อมรึยังหรือยังไม่ได้ซ่อม
    # ถ้ามี filter room_id
    if room_id:
        query = query.filter(DamageReport.room_id == room_id)

    # เรียงตามวันที่สร้าง (ใหม่สุดก่อน) แล้ว return
    return query.order_by(DamageReport.created_at.desc()).offset(skip).limit(limit).all()


# GET - ดึงรายงานตาม ID
@router.get("/{report_id}", response_model=DamageReportResponse)
def get_damage_report(report_id: UUID, db: Session = Depends(get_db)):
    """ดึงข้อมูลรายงานตาม ID"""
    
    report = db.query(DamageReport).filter(DamageReport.id == report_id).first()
    
    if not report:
        raise HTTPException(status_code=404, detail="Damage report not found")
    
    return report


# POST - สร้างรายงานใหม่ 
@router.post("/", response_model=DamageReportResponse, status_code=status.HTTP_201_CREATED)
def create_damage_report(
    report_data: DamageReportCreate,
    reporter_id: UUID = Query(..., description="Reporter ID from Supabase Auth"),
    db: Session = Depends(get_db)
):
    # STEP 1: ตรวจสอบว่าห้องมีจริง
    if not db.query(Room).filter(Room.id == report_data.room_id).first():
        raise HTTPException(status_code=404, detail="Room not found")
    
    # STEP 3: สร้าง report
    report = DamageReport(
        room_id=report_data.room_id,
        equipment_id=report_data.equipment_id, # อาจเป็น None ได้
        reporter_id=reporter_id,               # จาก Supabase Auth
        description=report_data.description,
        status=DamageStatus.REPORTED.value,     # เริ่มต้นเป็น "reported"
        created_by=reporter_id
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report
#  PATCH - เปลี่ยนสถานะเป็น "กำลังซ่อม" 
@router.patch("/{report_id}/in-progress", response_model=DamageReportResponse)
def mark_in_progress(report_id: UUID, db: Session = Depends(get_db)):
    report = db.query(DamageReport).filter(DamageReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Damage report not found")
    report.status = DamageStatus.IN_PROGRESS.value
    db.commit()
    db.refresh(report)
    return report

#  PATCH - เปลี่ยนสถานะเป็น "ซ่อมเสร็จ"
@router.patch("/{report_id}/resolve", response_model=DamageReportResponse)
def resolve_damage_report(report_id: UUID, db: Session = Depends(get_db)):
    report = db.query(DamageReport).filter(DamageReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Damage report not found")
    report.status = DamageStatus.RESOLVED.value
    db.commit()
    db.refresh(report)
    return report

# DELETE - ลบรายงาน
@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_damage_report(report_id: UUID, db: Session = Depends(get_db)):
    report = db.query(DamageReport).filter(DamageReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Damage report not found")
    db.delete(report)
    db.commit()