from pydantic import BaseModel


class SignalResponse(BaseModel):
    """Сигнал (обращение) студента.

    Student signal (request).

    Точная форма пока не подтверждена: для тестового аккаунта эндпоинт
    возвращает пустой список. Модель будет уточнена по первому непустому образцу.
    """


class SignalsResponse(BaseModel):
    signal_list: list[SignalResponse]


class SignalProblemResponse(BaseModel):
    """Проблема для сигнала.

    Signal problem entry.
    """

    id: int
    title: str | None = None


class SignalProblemsResponse(BaseModel):
    signal_problem_list: list[SignalProblemResponse]
