from enum import Enum


class JournalEndpoints(Enum):  # Thanks, neitan001!
    # ===  URL APIs of the official Journal server  ===

    # URL base
    BASE_API_URL = "https://msapi.top-academy.ru/api/v2"
    # URL for auth
    AUTH_URL = f"{BASE_API_URL}/auth/login"

    # == AUTO SEND APIs ==
    # URL для получения данных списка пар которые нужно оценить
    EVALUATION_LESSONS_LIST = f"{BASE_API_URL}/feedback/students/evaluate-lesson-list"
    # URL для отправки пар которые были оценены
    EVALUATION_LESSONS = f"{BASE_API_URL}/feedback/students/evaluate-lesson"

    # == USER DATA ==
    # URL для получения данных feedback (Отзывы о студенте)
    FEEDBACK_INFO = f"{BASE_API_URL}/reviews/index/list"
    # URL для получения данных о среднем балле студента
    METRIC_GRADE = f"{BASE_API_URL}/dashboard/chart/average-progress"
    # URL для получения данных о посещениях студента
    METRIC_ATTENDANCE = f"{BASE_API_URL}/dashboard/chart/attendance"
    # URL для получения данных о посещениях занятий и оценки
    STUDENT_VISITS = f"{BASE_API_URL}/progress/operations/student-visits"
    # URL для получения данных о количестве ДЗ
    STUDENT_HOMEWORK = f"{BASE_API_URL}/count/homework"
    #  URL для получения user info (По типу группы и т.д)
    USER_INFO = f"{BASE_API_URL}/settings/user-info"

    # == GROUP INFO ==
    # URL для получения данных с расписанием пар по дате
    SCHEDULE_URL = (
        f"{BASE_API_URL}/schedule/operations/get-by-date?date_filter={{date}}"
    )
    # URL для получения данных рейтинга группы студентов
    RATING_GROUP = f"{BASE_API_URL}/dashboard/progress/leader-group"
    # URL для получения данных рейтинга потока для студентов
    RATING_STREAM = f"{BASE_API_URL}/dashboard/progress/leader-stream"
