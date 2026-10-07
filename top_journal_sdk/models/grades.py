from datetime import date

from pydantic import BaseModel

from top_journal_sdk.models.attendance import AttendanceResponse


class GradeResponse(AttendanceResponse):
    """Оценка за занятие.

    Имеет ту же форму, что и запись посещаемости: датированная запись
    с баллами в журнале (date/points/previous_points/has_rasp).
    """

    pass


class GradesResponse(BaseModel):
    grade_list: list[GradeResponse]


class ClassAttendanceGradeResponse(BaseModel):
    date_visit: date
    lesson_number: int
    status_was: int
    spec_id: int
    teacher_name: str
    spec_name: str
    lesson_theme: str
    control_work_mark: int | None
    home_work_mark: int | None
    lab_work_mark: int | None
    class_work_mark: int | None
    practical_work_mark: int | None


class ClassAttendanceGradesResponse(BaseModel):
    class_attendance_grade_list: list[ClassAttendanceGradeResponse]
