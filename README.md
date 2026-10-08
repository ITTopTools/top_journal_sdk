# Top Journal SDK

Асинхронный Python SDK для работы с API журнала Top Academy (v0.2.0).

`top_journal_sdk` упрощает взаимодействие с системой журнала: пользователи, расписание,
оценки, посещаемость, домашние задания, дашборд, библиотека, маркет, портфолио,
профиль, оплата (чтение), сигналы, контакты и контент — через типизированные
Pydantic-модели и доменные исключения вместо голого HTTP.

## Требования

- Python 3.13+
- Зависимости ставятся автоматически: `beautifulsoup4`, `httpx`, `pydantic`, `rapid-api-client`

## Установка

```bash
pip install top-journal-sdk
# или
uv add top-journal-sdk
```

## Быстрый старт

```python
import asyncio
from datetime import date

from top_journal_sdk import TopJournalSDK


async def main() -> None:
    async with TopJournalSDK(timeout=30.0) as sdk:
        await sdk.login("username", "password")  # кеширует group_id/student_id

        user = await sdk.user.get_personal_info()
        print(user.full_name, user.group_name)

        schedule = await sdk.schedule.get_schedule_by_date(date.today())
        print(len(schedule.lesson_list))


asyncio.run(main())
```

После `login()` SDK кеширует контекст сессии (`current_group_id`, `student_id`):
методы вроде `sdk.homework.get_homeworks()` подставляют `group_id` сами,
явно передавать нужно только для чужой группы.

Токены обновляются автоматически: при `401` SDK один раз вызывает
`POST /auth/refresh` и повторяет запрос.

```python
import asyncio

from top_journal_sdk import TopJournalSDK
from top_journal_sdk.exceptions import JournalException


async def main() -> None:
    async with TopJournalSDK(timeout=30.0) as sdk:
        await sdk.login("username", "password")
        try:
            homeworks = await sdk.homework.get_homeworks()
            print("total:", homeworks.total)

            performance = await sdk.dashboard.get_academic_performance()
            print("average:", performance.total_all_time)
        except JournalException as e:
            print("API error:", e)


asyncio.run(main())
```

Полный пример на 16 шагов (все контроллеры) — в файле
[`example.py`](https://github.com/ITTopTools/top_journal_sdk/blob/dev/example.py).

## Контроллеры

| Свойство | Контроллер | Что умеет |
|---|---|---|
| `sdk.auth` | Auth | login, refresh токенов, сброс пароля |
| `sdk.user` | UserInfo | личная информация студента |
| `sdk.attendance` | Attendance | посещаемость |
| `sdk.grades` | Grades | средние оценки, оценки за посещаемость |
| `sdk.homework` | Homework | счетчики, список, теги, история групп |
| `sdk.schedule` | Schedule | расписание на день/месяц/диапазон, события месяца |
| `sdk.feedback` | Feedback | отзывы, соцотзывы, оценка академдня, просмотры материалов |
| `sdk.lesson_evaluation` | LessonEvaluation | уроки к оценке, теги, отправка оценки |
| `sdk.leaderboard` | Leaderboard | рейтинги группы и потока |
| `sdk.dashboard` | Dashboard | графики, успеваемость, активность, баллы рейтинга |
| `sdk.exams` | Exams | экзамены, четвертные оценки |
| `sdk.library` | Library | материалы, счетчики, интервью |
| `sdk.market` | Market | товары маркета |
| `sdk.portfolio` | Portfolio | работы, предметы и преподаватели для дизайна |
| `sdk.content` | Content | новости, сторис, языки, переводы, города |
| `sdk.profile` | Profile | настройки, достижения, документы, предметы, смена группы |
| `sdk.payment` | Payment | данные/история/график оплат (только чтение) |
| `sdk.signal` | Signal | сигналы и проблемы |
| `sdk.contacts` | Contacts | контакты филиала |

## Ошибки

Все транспортные ошибки преобразуются в доменные исключения
(`top_journal_sdk.exceptions`): `OutdatedJWTError` (401), `InvalidJWTError` (403),
`DataNotFoundError` (404), `RequestTimeoutError` (таймаут/408),
`InvalidAppKeyError` (410), `InvalidAuthDataError` (422),
`InternalServerError` (5xx). Ловите `JournalException` как базовый класс.

## Разработка

```bash
uv sync                  # базовые + dev-зависимости
uv run pytest -m "not live"   # офлайн-тесты
uv run pytest -m live          # live-тесты (нужны TOP_JOURNAL_USERNAME/PASSWORD)
uv run --with pyright pyright top_journal_sdk tests example.py  # strict, 0 ошибок
uv run ruff check top_journal_sdk tests example.py   # линтер, 0 ошибок
uv run ruff format --check top_journal_sdk tests example.py  # формат
uv run ty check top_journal_sdk tests example.py     # типы strict, 0 ошибок
uv build
```

Хуки pre-commit (`ruff-check --fix`, `ruff-format`, `ty`) ставятся через
`uv run pre-commit install` и гоняют то же самое при каждом коммите.

Live-тесты ходят в настоящий API тестовым студентом и скипаются без кредов.
Мутирующие вызовы (отправка оценок/комментариев, сброс пароля, смена группы)
вживую не гоняются — только shape-тесты тел запросов.

## Лицензия

MIT License

## Статус проекта

Активная разработка.
