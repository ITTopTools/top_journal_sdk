from datetime import date

from pydantic import BaseModel


class AttendanceResponse(BaseModel):
    date: date
    points: int | None
    previous_points: int | None
    has_rasp: bool | None


class AttendancesResponse(BaseModel):
    attendance_list: list[AttendanceResponse]
