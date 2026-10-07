"""Unit-тесты моделей Волны 3 на синтетических payload (без сети)."""

from top_journal_sdk.models.auth import ResetPasswordRequest
from top_journal_sdk.models.contacts import ContactsResponse
from top_journal_sdk.models.payment import (
    PaymentHistoryResponse,
    PaymentIndexResponse,
    PaymentScheduleResponse,
)
from top_journal_sdk.models.profile import (
    ProfileSettingsResponse,
    StudentAchievementResponse,
)
from top_journal_sdk.models.signal import SignalProblemResponse


def test_profile_settings() -> None:
    settings = ProfileSettingsResponse.model_validate(
        {
            "id": 39,
            "ful_name": "Name",
            "date_birth": "2006-03-05",
            "email": "a@b.c",
            "phones": [{"phone_type": 1, "phone_number": "79384102622"}],
            "links": [{"id": 1, "name": "Facebook", "valid": True}],
            "relatives": [],
            "azure": {"login": "x", "has_azure": True, "has_office": False},
            "is_email_verified": True,
        }
    )
    assert settings.phones[0].phone_number == "79384102622"
    assert settings.azure is not None and settings.azure.has_azure is True


def test_student_achievement() -> None:
    achievement = StudentAchievementResponse.model_validate(
        {
            "id": 1,
            "translate_key": "5_VISITS_WITHOUT_GAP",
            "is_active": True,
            "achieve_points": [{"id": 2, "points_count": 10}],
        }
    )
    assert achievement.achieve_points[0].points_count == 10


def test_payment_index() -> None:
    index = PaymentIndexResponse.model_validate(
        {
            "full_name": "Name",
            "city_id": 1,
            "legacy_payment": {"message_type": None},
            "payment": {"id": 5, "fio_stud": "N.O."},
            "one_c_code": "123",
        }
    )
    assert index.payment is not None and index.payment.id == 5


def test_payment_history() -> None:
    entry = PaymentHistoryResponse.model_validate(
        {"date": "2026-07-01", "amount": 100, "description": "desc", "type": 1}
    )
    assert entry.amount == 100


def test_payment_schedule() -> None:
    entry = PaymentScheduleResponse.model_validate(
        {
            "id": 1,
            "description": "desc",
            "price": 200,
            "payment_date": "2027-08-01",
            "status": 0,
        }
    )
    assert entry.price == 200


def test_signal_problem() -> None:
    problem = SignalProblemResponse.model_validate({"id": 1, "title": "Proposal"})
    assert problem.title == "Proposal"


def test_contacts() -> None:
    contacts = ContactsResponse.model_validate(
        {"adress": None, "vk": "https://vk.com/x", "teach_contacts": []}
    )
    assert contacts.vk == "https://vk.com/x"


def test_reset_password_request() -> None:
    body = ResetPasswordRequest(email="a@b.c")
    assert body.model_dump() == {"email": "a@b.c"}
