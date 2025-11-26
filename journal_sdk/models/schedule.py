from datetime import date, time

from pydantic import BaseModel

from journal_sdk.exceptions import LessonNotFoundError


class Lesson(BaseModel):
    date: date
    lesson: int
    started_at: time
    finished_at: time
    teacher_name: str
    subject_name: str
    room_name: str


class Schedule(BaseModel):
    lessons: list[Lesson]

    def lesson(self, number: int) -> Lesson | None:
        for lesson in self.lessons:
            if lesson.lesson == number:
                return lesson
        raise LessonNotFoundError(number)
