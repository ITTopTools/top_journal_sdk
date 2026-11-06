from enum import Enum


class JournalkaEndpoints(Enum):
    """
    Перечисление URL-адресов API journalka.top-academy.ru (v2).

    Enumeration of journalka.top-academy.ru API endpoints (v2).
    """

    # Базовый URL
    JOURNALKA_BASE_URL = "https://journalka.top-academy.ru"
    API_BASE_URL = "https://journalka.top-academy.ru/api"

    # == АУТЕНТИФИКАЦИЯ ==
    AUTH_LOGIN = "/api/auth/login"
    AUTH_LOGOUT = "/api/auth/logout"
    AUTH_REFRESH = "/api/auth/refresh"
    AUTH_SESSION_EXPIRED = "/api/auth/session-expired"

    # == ПУБЛИЧНОЕ ==
    PUBLIC_LANGUAGES = "/api/public/languages"
    PUBLIC_TRANSLATIONS = "/api/public/translations"

    # == ДАШБОРД / ПОЛЬЗОВАТЕЛЬ ==
    DASHBOARD_USER_INFO = "/api/dashboard/user-info"

    # == ДАШБОРД / ДОМАШНЯЯ СТРАНИЦА ==
    HOME_ATTENDANCE = "/api/dashboard/home/attendance"
    HOME_AVERAGE_PROGRESS = "/api/dashboard/home/average-progress"
    HOME_ACTIVITY = "/api/dashboard/home/activity"
    HOME_FUTURE_EXAMS = "/api/dashboard/home/future-exams"
    HOME_LEADER_GROUP = "/api/dashboard/home/leader-group"
    HOME_LEADER_GROUP_POINTS = "/api/dashboard/home/leader-group-points"
    HOME_LEADER_STREAM = "/api/dashboard/home/leader-stream"
    HOME_LEADER_STREAM_POINTS = "/api/dashboard/home/leader-stream-points"
    HOME_REVIEWS_COUNT = "/api/dashboard/home/reviews-count"
    HOME_ACHIEVEMENTS_COUNT = "/api/dashboard/home/achievements-count"

    # == ДАШБОРД / ОЦЕНКИ УРОКОВ ==
    LESSON_EVALUATIONS = "/api/dashboard/lesson-evaluations"

    # == ДАШБОРД / ПРОФИЛЬ ==
    PROFILE_SETTINGS = "/api/dashboard/profile/settings"
    PROFILE_DOCUMENTS = "/api/dashboard/profile/documents"
    PROFILE_DOCUMENTS_FIELDS = "/api/dashboard/profile/documents/fields"

    # == ДАШБОРД / ГРУППЫ ==
    GROUPS_CHANGE = "/api/dashboard/groups/change"

    # == ДАШБОРД / СТАРТАП ==
    STARTUP_CHECK_CANCELLATION = "/api/dashboard/startup/check-cancellation"
    STARTUP_DELAY_EMAIL_CONFIRMATION = "/api/dashboard/startup/delay-email-confirmation"
    STARTUP_DELAY_INTERVIEW = "/api/dashboard/startup/delay-interview"
    STARTUP_EMAIL_CONFIRMATION = "/api/dashboard/startup/email-confirmation"
    STARTUP_LESSON_EVALUATIONS = "/api/dashboard/startup/lesson-evaluations"
    STARTUP_OPENED_INTERVIEW = "/api/dashboard/startup/opened-interview"
    STARTUP_SIGNALS = "/api/dashboard/startup/signals"

    # == ДАШБОРД / СТАТИСТИКА ==
    STATS_HOMEWORK = "/api/dashboard/stats/homework"
    STATS_MATERIALS = "/api/dashboard/stats/materials"
    STATS_PAGE_COUNTERS = "/api/dashboard/stats/page-counters"
    STATS_SUPPORT = "/api/dashboard/stats/support"

    # == ДАШБОРД / СТОРИС ==
    STORIES = "/api/dashboard/stories"
    STORIES_LEAD = "/api/dashboard/stories/lead"

    # == ДАШБОРД / ПОДДЕРЖКА ==
    SUPPORT_REQUESTS = "/api/dashboard/support/requests/"

    # == ДАШБОРД / РАСПИСАНИЕ ==
    SCHEDULE = "/api/dashboard/schedule"
