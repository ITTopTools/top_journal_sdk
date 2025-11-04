from datetime import date, datetime
from enum import IntEnum
from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl


class GamingPointType(IntEnum):
    TOP_COINS = 1
    TOP_GEMS = 2


class GamingPoint(BaseModel):
    new_gaming_point_types__id: int = Field(..., ge=1, le=2)
    points: int = Field(..., ge=0)
    
    @property
    def type_name(self) -> str:
        names = {
            1: "Топ коины",
            2: "Топ гемы"
        }
        return names.get(self.new_gaming_point_types__id, "Неизвестно")


class UserInfo(BaseModel):
    gaming_points: List[GamingPoint]
    student_id: int
    full_name: str
    age: int
    gender: int = Field(..., ge=0, le=2)
    birthday: date
    photo: Optional[HttpUrl] = None
    current_group_id: int
    group_name: str
    current_group_status: int
    stream_id: int
    stream_name: str
    study_form_short_name: str
    achieves_count: int = Field(..., ge=0)
    registration_date: datetime
    last_date_visit: datetime
    
    @property
    def student_id_prop(self) -> int:
        return self.student_id
    
    @property
    def full_name_prop(self) -> str:
        return self.full_name.strip()
    
    @property
    def age_prop(self) -> int:
        return self.age
    
    @property
    def gender_prop(self) -> int:
        return self.gender
    
    @property
    def birthday_prop(self) -> date:
        return self.birthday
    
    @property
    def photo_url(self) -> str:
        return str(self.photo) if self.photo else ""
    
    @property
    def current_group_id_prop(self) -> int:
        return self.current_group_id
    
    @property
    def group_name_prop(self) -> str:
        return self.group_name
    
    @property
    def stream_id_prop(self) -> int:
        return self.stream_id
    
    @property
    def stream_name_prop(self) -> str:
        return self.stream_name
    
    @property
    def achieves_count_prop(self) -> int:
        return self.achieves_count
    
    @property
    def top_coins(self) -> int:
        for gp in self.gaming_points:
            if gp.new_gaming_point_types__id == GamingPointType.TOP_COINS:
                return gp.points
        return 0
    
    @property
    def top_gems(self) -> int:
        for gp in self.gaming_points:
            if gp.new_gaming_point_types__id == GamingPointType.TOP_GEMS:
                return gp.points
        return 0
    
    @property
    def total_gaming_points(self) -> int:
        return sum(gp.points for gp in self.gaming_points)
    
    @property
    def registration_date_prop(self) -> datetime:
        return self.registration_date
    
    @property
    def last_date_visit_prop(self) -> datetime:
        return self.last_date_visit
