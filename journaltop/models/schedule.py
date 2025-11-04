from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, time
from ..errors.journal_exceptions import LessonNotFoundError

class Lesson(BaseModel):
    date: date
    lesson: int = Field(..., ge=1, le=8)
    started_at: time
    finished_at: time
    teacher_name: str
    subject_name: str
    room_name: str


class Schedule(BaseModel):
    lessons: List[Lesson]
    
    def lesson(self, number: int) -> Optional[Lesson]:
        for lesson in self.lessons:
            if lesson.lesson == number:
                return lesson
        raise LessonNotFoundError(number)
