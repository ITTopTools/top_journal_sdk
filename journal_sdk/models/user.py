from datetime import date, datetime
from enum import IntEnum

from pydantic import BaseModel, HttpUrl


class GamingPointType(IntEnum):
    TOP_COINS = 1
    TOP_GEMS = 2


class GamingPointResponse(BaseModel):
    new_gaming_point_types__id: GamingPointType
    points: int

    @property
    def type_name(self) -> str:
        names = {1: "Топ коины", 2: "Топ гемы"}
        return names.get(self.new_gaming_point_types__id, "Неизвестно")


class UserResponse(BaseModel):
    gaming_points: list[GamingPointResponse]
    student_id: int
    full_name: str
    age: int
    gender: int
    birthday: date
    photo: HttpUrl | None
    current_group_id: int
    group_name: str
    current_group_status: int
    stream_id: int
    stream_name: str
    study_form_short_name: str
    achieves_count: int
    registration_date: datetime
    last_date_visit: datetime

    @property
    def photo_url(self) -> str:
        return str(self.photo) if self.photo else ""

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
