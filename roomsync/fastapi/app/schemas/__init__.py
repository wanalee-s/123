from app.schemas.room import RoomCreate, RoomUpdate, RoomResponse, RoomWithEquipments
from app.schemas.equipment import EquipmentCreate, EquipmentUpdate, EquipmentResponse
from app.schemas.room_equipment import RoomEquipmentCreate, RoomEquipmentResponse
from app.schemas.booking import BookingCreate, BookingUpdate, BookingResponse
from app.schemas.damage_report import DamageReportCreate, DamageReportUpdate, DamageReportResponse
# Profile
from app.schemas.profile import (
    UserRoleEnum,
    ProfileCreate,
    ProfileUpdate,
    ProfileResponse,
    ProfileDetail,
    ProfileSummary,
)