"""
Модуль контроллеров для взаимодействия с API журнала Top Academy.

Controller module for interacting with Top Academy journal API.
"""

from top_journal_sdk.controllers.attendance import AttendanceController
from top_journal_sdk.controllers.auth import AuthController
from top_journal_sdk.controllers.evaluation import LessonEvaluationController
from top_journal_sdk.controllers.feedback import FeedbackController
from top_journal_sdk.controllers.grades import GradesController
from top_journal_sdk.controllers.homework import HomeworkController
from top_journal_sdk.controllers.leaderboard import LeaderboardController
from top_journal_sdk.controllers.schedule import ScheduleController
from top_journal_sdk.controllers.user import UserInfoController

__all__ = [
    "AuthController",
    "UserInfoController",
    "GradesController",
    "AttendanceController",
    "HomeworkController",
    "ScheduleController",
    "FeedbackController",
    "LessonEvaluationController",
    "LeaderboardController",
]
