from top_journal_sdk._models import APIModel, UnconfirmedResponse


class SignalResponse(UnconfirmedResponse):
    """Сигнал (обращение) студента.

    Student signal (request).

    Точная форма пока не подтверждена: для тестового аккаунта эндпоинт
    возвращает пустой список. Модель будет уточнена по первому непустому образцу.
    """


class SignalsResponse(APIModel):
    signal_list: list[SignalResponse]


class SignalProblemResponse(APIModel):
    """Проблема для сигнала.

    Signal problem entry.
    """

    id: int
    title: str | None = None


class SignalProblemsResponse(APIModel):
    signal_problem_list: list[SignalProblemResponse]
