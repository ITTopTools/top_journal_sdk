from enum import Enum


class JournalEndpoints(Enum):
    """
    Перечисление URL-адресов API журнала Top Academy.

    Enumeration of Top Academy journal API endpoints.
    """

    # Базовый URL журнала
    # Journal base URL
    JOURNAL_BASE_URL = "https://journal.top-academy.ru"

    # Базовый URL API
    # API base URL
    API_BASE_URL = "https://msapi.top-academy.ru/api/v2"

    # Эндпоинт аутентификации
    # Authentication endpoint
    AUTH = "/auth/login"

    # Эндпоинт для получения списка пар, которые нужно оценить
    # Endpoint for getting the list of lessons that need to be evaluated
    EVALUATION_LESSONS_LIST = "/feedback/students/evaluate-lesson-list"

    # Эндпоинт для отправки оцененных пар
    # Endpoint for submitting evaluated lessons
    EVALUATION_LESSONS = "/feedback/students/evaluate-lesson"

    # == ДАННЫЕ ПОЛЬЗОВАТЕЛЯ ==
    # == USER DATA ==

    # Эндпоинт для получения данных отзывов о студенте
    # Endpoint for getting feedback data (Reviews about the student)
    FEEDBACK_INFO = "/reviews/index/list"

    # Эндпоинт для получения данных о среднем балле студента
    # Endpoint for getting student's average grade data
    METRIC_GRADE = "/dashboard/chart/average-progress"

    # Эндпоинт для получения данных о посещаемости студента
    # Endpoint for getting student attendance data
    METRIC_ATTENDANCE = "/dashboard/chart/attendance"

    # Эндпоинт для получения данных о посещаемости занятий и оценках
    # Endpoint for getting data about class attendance and grades
    STUDENT_VISITS = "/progress/operations/student-visits"

    # Эндпоинт для получения данных о количестве домашних заданий
    # Endpoint for getting data about the number of homework assignments
    STUDENT_HOMEWORK = "/count/homework"

    # Эндпоинт для получения информации о пользователе (группа и т.д.)
    # Endpoint for getting user info (group, etc.)
    USER_INFO = "/settings/user-info"

    # == ИНФОРМАЦИЯ О ГРУППЕ ==
    # == GROUP INFO ==

    # Эндпоинт для получения расписания пар по дате
    # Endpoint for getting lesson schedule by date
    SCHEDULE = "/schedule/operations/get-by-date?date_filter={{date}}"

    # Эндпоинт для получения данных рейтинга группы студентов
    # Endpoint for getting student group rating data
    RATING_GROUP = "/dashboard/progress/leader-group"

    # Эндпоинт для получения данных рейтинга потока студентов
    # Endpoint for getting student stream rating data
    RATING_STREAM = "/dashboard/progress/leader-stream"
