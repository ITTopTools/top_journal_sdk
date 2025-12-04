from datetime import date, time

from pydantic import BaseModel

from top_journal_sdk.exceptions import LessonNotFoundError


class LessonResponse(BaseModel):
    date: date
    lesson: int
    started_at: time
    finished_at: time
    teacher_name: str
    subject_name: str
    room_name: str


class ScheduleResponse(BaseModel):
    lesson_list: list[LessonResponse]

    def lesson(self, number: int) -> LessonResponse | None:
        for lesson in self.lesson_list:
            if lesson.lesson == number:
                return lesson
        raise LessonNotFoundError(number)
