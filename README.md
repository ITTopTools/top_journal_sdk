# Top Journal SDK

Асинхронный Python SDK для работы с API журнала Top Academy (v0.4.0).

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

Для доступа с IP, на которых включается DDoS-Guard, установите браузер:

```bash
pip install "top-journal-sdk[browser]"
playwright install chromium
```

Обе версии SDK автоматически используют Chromium при `403`, `429`, HTML-странице
DDoS-Guard или ошибке установки соединения. Браузер открывает сайт, проходит
проверку и выполняет исходный запрос, включая запрос логина, через `fetch` внутри
страницы. Cookies сессии сохраняются в HTTP-клиенте для следующих запросов.
Ответы `401`/`422` на логин не запускают повторный браузерный вход.
Без установленного браузера блокировка сопровождается ошибкой с инструкцией
установки. Отключить этот механизм можно через `TopJournalSDK(browser_fallback=False)`
или `TopJournalSDKV2(auto_refresh_ddg=False)`.

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
from top_journal_sdk.v1.exceptions import JournalException


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
[`example.py`](https://github.com/ITTopTools/top_journal_sdk/blob/main/example.py).

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

## Версия v2 (journalka.top-academy.ru)

Помимо основного API (`journal.top-academy.ru`), SDK поддерживает альтернативный
поддомен **journalka.top-academy.ru** через класс `TopJournalSDKV2`.

Установка с опциональной зависимостью для браузера (нужна только для
авто-получения `__ddg*` кук DDoS-Guard):

```bash
pip install top-journal-sdk
# или с браузером для авто-обновления кук защиты:
pip install "top-journal-sdk[browser]"

playwright install chromium
```

### Быстрый старт v2

```python
import asyncio

from top_journal_sdk import TopJournalSDKV2


async def main() -> None:
    async with TopJournalSDKV2(timeout=30.0) as sdk:
        # Логин — токены приходят в cookies (не Bearer-заголовок)
        await sdk.login("username", "password")

        user = await sdk.user.get_personal_info()
        print(user.user.full_name, user.user.group_name)

        attendance = await sdk.dashboard.get_home_attendance()
        for item in attendance.items:
            print(item.date, item.points)

        schedule = await sdk.dashboard.get_schedule(
            scope="week",
            date_start="2026-10-19",
            date_end="2026-10-25",
        )
        print(len(schedule.items), "занятий")


asyncio.run(main())
```

### Контроллеры v2

| Свойство | Контроллер | Что умеет |
|---|---|---|
| `sdk.auth` | Auth | login, logout, refresh |
| `sdk.user` | User | личная информация студента |
| `sdk.dashboard` | Dashboard | посещаемость, прогресс, активность, рейтинг, сторис, расписание, статистика |
| `sdk.profile` | Profile | настройки, документы, смена группы |

### Особенности v2

- **Авторизация через cookies** — `POST /api/auth/login` возвращает `Set-Cookie`
  с `journal_access_token`, `journal_refresh_token` и т.д. SDK сохраняет их
  автоматически и отправляет в каждом запросе.
- **DDoS-Guard (`__ddg*` куки)** — при блокировке SDK выполняет запрос в Chromium,
  включая логин, и сохраняет cookies. Для `401` защищённых методов также доступно
  обновление `__ddg*` через Playwright (нужна зависимость `[browser]` и Chromium).
  Можно передать куки вручную через `sdk.set_ddg_cookies({...})`.
- **Авто-обновление сессии** — при `401` SDK один раз обновляет сессию через
  `POST /api/auth/refresh`, затем при необходимости обновляет `__ddg*` куки
  и повторяет исходный запрос.
- **Ошибки** — v2 пробрасывает `httpx.HTTPStatusError`; доменные исключения
  `top_journal_sdk.v1.exceptions` относятся к API v1.
- Методы возвращают **типизированные Pydantic-модели**. Для ответов, формат
  которых ещё не описан, возвращается `dict[str, Any]` / `list[dict[str, Any]]`.
- Методы `get_startup_delay_email_confirmation()` и
  `get_startup_delay_interview()` пока экспериментальные: HTTP-метод и формат
  запроса ещё не подтверждены на реальном API.

## Миграция 0.3 → 0.4

Модули v1 переехали в `top_journal_sdk.v1`, v2 — в `top_journal_sdk.v2`.
Классы `TopJournalSDK` и `TopJournalSDKV2` по-прежнему импортируются из корня.

| Было | Стало |
|---|---|
| `top_journal_sdk.exceptions` | `top_journal_sdk.v1.exceptions` |
| `top_journal_sdk.models.*` | `top_journal_sdk.v1.models.*` |
| `top_journal_sdk.controllers.*` | `top_journal_sdk.v1.controllers.*` |
| `top_journal_sdk.enums.*` | `top_journal_sdk.v1.enums.*` |
| `top_journal_sdk.session` | `top_journal_sdk.v1.session` |
| `top_journal_sdk.utils.app_key` | `top_journal_sdk.v1.utils.app_key` |

## Ошибки

Транспортные ошибки v1 преобразуются в доменные исключения
(`top_journal_sdk.v1.exceptions`): `OutdatedJWTError` (401), `InvalidJWTError` (403),
`DataNotFoundError` (404), `RequestTimeoutError` (таймаут/408),
`InvalidAppKeyError` (410), `InvalidAuthDataError` (422),
`InternalServerError` (5xx). Ловите `JournalException` как базовый класс.

## Разработка

```bash
uv sync                  # базовые + dev-зависимости
uv run pytest            # офлайн-тесты (live исключены через addopts)
uv run pytest -m live    # live-тесты (нужны TOP_JOURNAL_USERNAME/PASSWORD или .env)
uv run pytest --cov=top_journal_sdk  # покрытие
uv run --with pyright pyright top_journal_sdk tests example.py  # strict, 0 ошибок
uv run ruff check top_journal_sdk tests example.py   # линтер, 0 ошибок
uv run ruff format --check top_journal_sdk tests example.py  # формат
uv run ty check top_journal_sdk tests example.py     # типы strict, 0 ошибок
uv build
```

Хуки pre-commit (`ruff-check --fix`, `ruff-format`, `ty`) ставятся через
`uv run pre-commit install` и гоняют то же самое при каждом коммите.

Live-тесты ходят в настоящий API тестовым студентом и скипаются без кредов.
Файл `.env` в корне репозитория подхватывается автоматически. Мутирующие вызовы
(отправка оценок/комментариев, сброс пароля, смена группы) вживую не гоняются —
только shape-тесты тел запросов.

## Лицензия

MIT License

## Статус проекта

Активная разработка.
