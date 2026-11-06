from datetime import date

from top_journal_sdk._models import APIModel


class AttendanceResponse(APIModel):
    date: date
    points: int | None
    previous_points: int | None
    has_rasp: bool | None


class AttendancesResponse(APIModel):
    attendance_list: list[AttendanceResponse]
