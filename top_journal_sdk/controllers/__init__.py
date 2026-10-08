"""
Модуль контроллеров для взаимодействия с API журнала Top Academy.

Controller module for interacting with Top Academy journal API.
"""

from top_journal_sdk.controllers.attendance import AttendanceController
from top_journal_sdk.controllers.auth import AuthController
from top_journal_sdk.controllers.contacts import ContactsController
from top_journal_sdk.controllers.content import ContentController
from top_journal_sdk.controllers.dashboard import DashboardController
from top_journal_sdk.controllers.evaluation import LessonEvaluationController
from top_journal_sdk.controllers.exams import ExamsController
from top_journal_sdk.controllers.feedback import FeedbackController
from top_journal_sdk.controllers.grades import GradesController
from top_journal_sdk.controllers.homework import HomeworkController
from top_journal_sdk.controllers.leaderboard import LeaderboardController
from top_journal_sdk.controllers.library import LibraryController
from top_journal_sdk.controllers.market import MarketController
from top_journal_sdk.controllers.payment import PaymentController
from top_journal_sdk.controllers.portfolio import PortfolioController
from top_journal_sdk.controllers.profile import ProfileController
from top_journal_sdk.controllers.schedule import ScheduleController
from top_journal_sdk.controllers.signal import SignalController
from top_journal_sdk.controllers.user import UserInfoController

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
