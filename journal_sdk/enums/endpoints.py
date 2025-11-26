from enum import Enum


class JournalEndpoints(Enum):
    """
    Перечисление URL-адресов API журнала Top Academy.

    Enumeration of Top Academy journal API endpoints.
    """

    # Базовые URL
    # Base URLs
    JOURNAL_BASE_URL = "https://journal.top-academy.ru"
    API_BASE_URL = "https://msapi.top-academy.ru/api/v2"

    # == АУТЕНТИФИКАЦИЯ ==
    # == AUTHENTICATION ==

    # Эндпоинт аутентификации
    # Authentication endpoint
    AUTH_LOGIN = "/auth/login"

    # == РАБОТА С ОЦЕНКАМИ ЗАНЯТИЙ ==
    # == EVALUATION WORK LESSONS ==

    # Эндпоинт для получения списка пар, которые нужно оценить
    # Endpoint for getting the list of lessons that need to be evaluated
    LESSONS_TO_EVALUATE = "/feedback/students/evaluate-lesson-list"

    # Эндпоинт для отправки оцененных пар
    # Endpoint for submitting evaluated lessons
    SUBMIT_EVALUATION_LESSONS = "/feedback/students/evaluate-lesson"

    # == ДАННЫЕ ПОЛЬЗОВАТЕЛЯ ==
    # == USER DATA ==

    # Эндпоинт для получения информации о пользователе (группа и т.д.)
    # Endpoint for getting user info (group, etc.)
    USER_PERSONAL_INFO = "/settings/user-info"

    # Эндпоинт для получения данных отзывов о студенте
    # Endpoint for getting feedback data (Reviews about the student)
    STUDENT_REVIEWS = "/reviews/index/list"

    # Эндпоинт для получения данных о среднем балле студента
    # Endpoint for getting student's average grade data
    AVERAGE_GRADE = "/dashboard/chart/average-progress"

    # Эндпоинт для получения данных о посещаемости студента
    # Endpoint for getting student attendance data
    ATTENDANCE_DATA = "/dashboard/chart/attendance"

    # Эндпоинт для получения данных о посещаемости занятий и оценках
    # Endpoint for getting data about class attendance and grades
    CLASS_ATTENDANCE_GRADES = "/progress/operations/student-visits"

    # Эндпоинт для получения данных о количестве домашних заданий
    # Endpoint for getting data about the number of homework assignments
    HOMEWORK_COUNT = "/count/homework"

    # Эндпоинт для получения расписания пар по дате
    # Endpoint for getting lesson schedule by date
    SCHEDULE_BY_DATE = "/schedule/operations/get-by-date?date_filter={{date}}"

    # == ИНФОРМАЦИЯ О ГРУППЕ ==
    # == GROUP INFO ==

    # Эндпоинт для получения данных рейтинга группы студентов
    # Endpoint for getting student group rating data
    GROUP_LEADERBOARD = "/dashboard/progress/leader-group"

    # Эндпоинт для получения данных рейтинга потока студентов
    # Endpoint for getting student stream rating data
    STREAM_LEADERBOARD = "/dashboard/progress/leader-stream"
