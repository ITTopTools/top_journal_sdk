from enum import Enum


class JournalEndpoints(Enum):
    """
    Перечисление URL-адресов API журнала Top Academy.

    Enumeration of Top Academy journal API endpoints.

    Attributes:
        JOURNAL_BASE_URL (str): Базовый URL журнала Top Academy.
        API_BASE_URL (str): Базовый URL API Top Academy.
        AUTH_LOGIN (str): Эндпоинт аутентификации.
        AUTH_REFRESH (str): Эндпоинт обновления токенов.
        LESSONS_TO_EVALUATE (str): Эндпоинт для получения списка пар, которые нужно оценить.
        SUBMIT_EVALUATION_LESSONS (str): Эндпоинт для отправки оцененных пар.
        EVALUATION_LESSON_TAGS (str): Эндпоинт для получения тегов оценки занятий.
        USER_PERSONAL_INFO (str): Эндпоинт для получения информации о пользователе.
        STUDENT_REVIEWS (str): Эндпоинт для получения данных отзывов о студенте.
        AVERAGE_GRADE (str): Эндпоинт для получения данных о среднем балле студента.
        ATTENDANCE_DATA (str): Эндпоинт для получения данных о посещаемости студента.
        CLASS_ATTENDANCE_GRADES (str): Эндпоинт для получения данных о посещаемости занятий и оценках.
        HOMEWORK_COUNT (str): Эндпоинт для получения данных о количестве домашних заданий.
        HOMEWORK_LIST (str): Эндпоинт для получения списка домашних заданий.
        HOMEWORK_EVALUATION_TAGS (str): Эндпоинт для получения тегов оценки домашних заданий.
        HOMEWORK_GROUP_HISTORY (str): Эндпоинт для получения истории групп по домашним заданиям.
        SCHEDULE_BY_DATE (str): Эндпоинт для получения расписания пар по дате.
        SCHEDULE_BY_MONTH (str): Эндпоинт для получения расписания пар за месяц.
        SCHEDULE_BY_DATE_RANGE (str): Эндпоинт для получения расписания пар за диапазон дат.
        SCHEDULE_MONTH_EVENTS (str): Эндпоинт для получения событий месяца.
        DASHBOARD_CHART_PROGRESS (str): Эндпоинт графика прогресса.
        DASHBOARD_FUTURE_EXAMS (str): Эндпоинт будущих экзаменов.
        DASHBOARD_ACADEMIC_PERFORMANCE (str): Эндпоинт академической успеваемости.
        DASHBOARD_ACTIVITY (str): Эндпоинт активности студента.
        DASHBOARD_ATTENDANCE_STATISTIC (str): Эндпоинт статистики посещаемости.
        DASHBOARD_LEADER_GROUP_POINTS (str): Эндпоинт баллов рейтинга группы.
        DASHBOARD_LEADER_STREAM_POINTS (str): Эндпоинт баллов рейтинга потока.
        DASHBOARD_PAGE_COUNTERS (str): Эндпоинт счетчиков страниц.
        STUDENT_EXAMS (str): Эндпоинт экзаменов студента.
        SCHOOL_QUARTERLY_GRADES (str): Эндпоинт четвертных оценок.
        SOCIAL_REVIEW_LIST (str): Эндпоинт списка социальных отзывов.
        SOCIAL_REVIEW_SCREEN (str): Эндпоинт отправки скриншота отзыва.
        ACADEMY_DAY_EVALUATE (str): Эндпоинт формы оценки академического дня.
        ACADEMY_DAY_COMMENT (str): Эндпоинт комментария к академическому дню.
        SET_VIEW_MATERIALS (str): Эндпоинт отметки просмотра материала.
        LIBRARY_LIST (str): Эндпоинт списка материалов библиотеки.
        LIBRARY_COUNT (str): Эндпоинт счетчиков библиотеки.
        LIBRARY_QUIZ_INTERVIEW (str): Эндпоинт открытого интервью библиотеки.
        MARKET_PRODUCT_LIST (str): Эндпоинт списка товаров маркета.
        PORTFOLIO_LIST (str): Эндпоинт списка портфолио.
        PORTFOLIO_DESIGN_SPECS (str): Эндпоинт предметов для дизайна портфолио.
        PORTFOLIO_DESIGN_TEACHERS (str): Эндпоинт преподавателей для дизайна.
        NEWS_LATEST (str): Эндпоинт последних новостей.
        STORIES_LIST (str): Эндпоинт сторис.
        STORIES_LOGIN_PAGE (str): Эндпоинт сторис страницы входа.
        PUBLIC_LANGUAGES (str): Эндпоинт языков.
        PUBLIC_TRANSLATIONS (str): Эндпоинт переводов.
        PUBLIC_CITIES (str): Эндпоинт городов.
        GROUP_LEADERBOARD (str): Эндпоинт для получения данных рейтинга группы студентов.
        STREAM_LEADERBOARD (str): Эндпоинт для получения данных рейтинга потока студентов.
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

    # Эндпоинт обновления токенов
    # Token refresh endpoint
    AUTH_REFRESH = "/auth/refresh"

    # == РАБОТА С ОЦЕНКАМИ ЗАНЯТИЙ ==
    # == EVALUATION WORK LESSONS ==

    # Эндпоинт для получения списка пар, которые нужно оценить
    # Endpoint for getting the list of lessons that need to be evaluated
    LESSONS_TO_EVALUATE = "/feedback/students/evaluate-lesson-list"

    # Эндпоинт для отправки оцененных пар
    # Endpoint for submitting evaluated lessons
    SUBMIT_EVALUATION_LESSONS = "/feedback/students/evaluate-lesson"

    # Эндпоинт для получения тегов оценки занятий
    # Endpoint for getting evaluation lesson tags
    EVALUATION_LESSON_TAGS = "/public/tags"

    # Эндпоинт для получения списка социальных отзывов
    # Endpoint for getting the social review list
    SOCIAL_REVIEW_LIST = "/feedback/social-review/get-review-list"

    # Эндпоинт для отправки скриншота отзыва
    # Endpoint for submitting a review screenshot
    SOCIAL_REVIEW_SCREEN = "/feedback/social-review/screen-review"

    # Эндпоинт формы оценки академического дня
    # Academy day evaluation form endpoint
    ACADEMY_DAY_EVALUATE = "/feedback/students/evaluate-academy-day"

    # Эндпоинт отправки комментария к академическому дню
    # Academy day comment submission endpoint
    ACADEMY_DAY_COMMENT = "/feedback/students/comment-academy-day"

    # Эндпоинт отметки просмотра материала
    # Material view marking endpoint
    SET_VIEW_MATERIALS = "/count/set-view-materials"

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

    # Эндпоинт для получения списка домашних заданий
    # Endpoint for getting the homework assignment list
    HOMEWORK_LIST = "/homework/operations/list"

    # Эндпоинт для получения тегов оценки домашних заданий
    # Endpoint for getting homework evaluation tags
    HOMEWORK_EVALUATION_TAGS = "/homework/evaluation/operations/get-tags"

    # Эндпоинт для получения истории групп по домашним заданиям
    # Endpoint for getting homework group history
    HOMEWORK_GROUP_HISTORY = "/homework/settings/group-history"

    # Эндпоинт для получения расписания пар по дате
    # Endpoint for getting lesson schedule by date
    SCHEDULE_BY_DATE = "/schedule/operations/get-by-date"

    # Эндпоинт для получения расписания пар за месяц
    # Endpoint for getting monthly lesson schedule
    SCHEDULE_BY_MONTH = "/schedule/operations/get-month"

    # Эндпоинт для получения расписания пар за диапазон дат
    # Endpoint for getting lesson schedule by date range
    SCHEDULE_BY_DATE_RANGE = "/schedule/operations/get-by-date-range"

    # Эндпоинт для получения событий месяца
    # Endpoint for getting month events
    SCHEDULE_MONTH_EVENTS = "/schedule/operations/month-events"

    # == ДАШБОРД И ПРОГРЕСС ==
    # == DASHBOARD & PROGRESS ==

    # Эндпоинт графика прогресса
    # Progress chart endpoint
    DASHBOARD_CHART_PROGRESS = "/dashboard/chart/progress"

    # Эндпоинт будущих экзаменов
    # Future exams endpoint
    DASHBOARD_FUTURE_EXAMS = "/dashboard/info/future-exams"

    # Эндпоинт академической успеваемости
    # Academic performance endpoint
    DASHBOARD_ACADEMIC_PERFORMANCE = "/dashboard/progress/academic-performance"

    # Эндпоинт активности студента
    # Student activity endpoint
    DASHBOARD_ACTIVITY = "/dashboard/progress/activity"

    # Эндпоинт статистики посещаемости
    # Attendance statistic endpoint
    DASHBOARD_ATTENDANCE_STATISTIC = "/dashboard/progress/attendance-statistic"

    # Эндпоинт баллов рейтинга группы
    # Group leaderboard points endpoint
    DASHBOARD_LEADER_GROUP_POINTS = "/dashboard/progress/leader-group-points"

    # Эндпоинт баллов рейтинга потока
    # Stream leaderboard points endpoint
    DASHBOARD_LEADER_STREAM_POINTS = "/dashboard/progress/leader-stream-points"

    # Эндпоинт счетчиков страниц
    # Page counters endpoint
    DASHBOARD_PAGE_COUNTERS = "/count/page-counters"

    # == ЭКЗАМЕНЫ ==
    # == EXAMS ==

    # Эндпоинт экзаменов студента
    # Student exams endpoint
    STUDENT_EXAMS = "/progress/operations/student-exams"

    # Эндпоинт четвертных оценок
    # Quarterly grades endpoint
    SCHOOL_QUARTERLY_GRADES = "/progress/operations/school-quarterly-grades"

    # == БИБЛИОТЕКА ==
    # == LIBRARY ==

    # Эндпоинт списка материалов библиотеки
    # Library materials list endpoint
    LIBRARY_LIST = "/library/operations/list"

    # Эндпоинт счетчиков библиотеки
    # Library counters endpoint
    LIBRARY_COUNT = "/count/library"

    # Эндпоинт открытого интервью библиотеки
    # Library opened interview endpoint
    LIBRARY_QUIZ_INTERVIEW = "/library/quiz/opened-interview"

    # == МАРКЕТ ==
    # == MARKET ==

    # Эндпоинт списка товаров маркета
    # Market product list endpoint
    MARKET_PRODUCT_LIST = "/market/customer/product/list"

    # == ПОРТФОЛИО ==
    # == PORTFOLIO ==

    # Эндпоинт списка портфолио
    # Portfolio list endpoint
    PORTFOLIO_LIST = "/portfolio/operations/list"

    # Эндпоинт предметов для дизайна портфолио
    # Portfolio design specs endpoint
    PORTFOLIO_DESIGN_SPECS = "/portfolio/operations/design-specs"

    # Эндпоинт преподавателей для дизайна портфолио
    # Portfolio design teachers endpoint
    PORTFOLIO_DESIGN_TEACHERS = "/portfolio/operations/design-teachers"

    # == КОНТЕНТ ==
    # == CONTENT ==

    # Эндпоинт последних новостей
    # Latest news endpoint
    NEWS_LATEST = "/news/operations/latest-news"

    # Эндпоинт сторис
    # Stories endpoint
    STORIES_LIST = "/story/operations/get-stories"

    # Эндпоинт сторис страницы входа
    # Login page stories endpoint
    STORIES_LOGIN_PAGE = "/story/operations/get-login-page-stories"

    # Эндпоинт языков
    # Languages endpoint
    PUBLIC_LANGUAGES = "/public/languages"

    # Эндпоинт переводов
    # Translations endpoint
    PUBLIC_TRANSLATIONS = "/public/translations"

    # Эндпоинт городов
    # Cities endpoint
    PUBLIC_CITIES = "/public/cities"

    # == ИНФОРМАЦИЯ О ГРУППЕ ==
    # == GROUP INFO ==

    # Эндпоинт для получения данных рейтинга группы студентов
    # Endpoint for getting student group rating data
    GROUP_LEADERBOARD = "/dashboard/progress/leader-group"

    # Эндпоинт для получения данных рейтинга потока студентов
    # Endpoint for getting student stream rating data
    STREAM_LEADERBOARD = "/dashboard/progress/leader-stream"
