from datetime import date, time

from top_journal_sdk._models import APIModel, UnconfirmedResponse
from top_journal_sdk.v1.exceptions import LessonNotFoundError


class LessonResponse(APIModel):
    date: date
    lesson: int
    started_at: time
    finished_at: time
    teacher_name: str
    subject_name: str
    room_name: str


class ScheduleResponse(APIModel):
    lesson_list: list[LessonResponse]

    def lesson(self, number: int) -> LessonResponse:
        for lesson in self.lesson_list:
            if lesson.lesson == number:
                return lesson
        raise LessonNotFoundError(number)


class MonthEventResponse(UnconfirmedResponse):
    """Событие месяца.

    Month event.

    Точная форма пока не подтверждена: для тестового аккаунта эндпоинт
    возвращает пустой список. Неизвестные поля сохраняются без потерь;
    модель будет уточнена по первому непустому образцу.
    """


class MonthEventsResponse(APIModel):
    month_event_list: list[MonthEventResponse]
