"""
Модуль контроллеров для взаимодействия с API журнала Top Academy.

Controller module for interacting with Top Academy journal API.
"""

from top_journal_sdk.v1.controllers.attendance import AttendanceController
from top_journal_sdk.v1.controllers.auth import AuthController
from top_journal_sdk.v1.controllers.contacts import ContactsController
from top_journal_sdk.v1.controllers.content import ContentController
from top_journal_sdk.v1.controllers.dashboard import DashboardController
from top_journal_sdk.v1.controllers.evaluation import LessonEvaluationController
from top_journal_sdk.v1.controllers.exams import ExamsController
from top_journal_sdk.v1.controllers.feedback import FeedbackController
from top_journal_sdk.v1.controllers.grades import GradesController
from top_journal_sdk.v1.controllers.homework import HomeworkController
from top_journal_sdk.v1.controllers.leaderboard import LeaderboardController
from top_journal_sdk.v1.controllers.library import LibraryController
from top_journal_sdk.v1.controllers.market import MarketController
from top_journal_sdk.v1.controllers.payment import PaymentController
from top_journal_sdk.v1.controllers.portfolio import PortfolioController
from top_journal_sdk.v1.controllers.profile import ProfileController
from top_journal_sdk.v1.controllers.schedule import ScheduleController
from top_journal_sdk.v1.controllers.signal import SignalController
from top_journal_sdk.v1.controllers.user import UserInfoController

__all__ = [
    "AttendanceController",
    "AuthController",
    "ContactsController",
    "ContentController",
    "DashboardController",
    "ExamsController",
    "FeedbackController",
    "GradesController",
    "HomeworkController",
    "LeaderboardController",
    "LessonEvaluationController",
    "LibraryController",
    "MarketController",
    "PaymentController",
    "PortfolioController",
    "ProfileController",
    "ScheduleController",
    "SignalController",
    "UserInfoController",
]
