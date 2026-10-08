from datetime import date, datetime

from pydantic import HttpUrl

from top_journal_sdk.models.user import (
    GamingPointResponse,
    GamingPointType,
    UserResponse,
)


def _user(photo: HttpUrl | None = None) -> UserResponse:
    return UserResponse(
        gaming_points=[
            GamingPointResponse(new_gaming_point_types__id=GamingPointType.TOP_COINS, points=10),
            GamingPointResponse(new_gaming_point_types__id=GamingPointType.TOP_GEMS, points=3),
        ],
        student_id=1,
        full_name="Test Student",
        age=20,
        gender=1,
        birthday=date(2006, 1, 1),
        photo=photo,
        current_group_id=1,
        group_name="Group",
        current_group_status=1,
        stream_id=1,
        stream_name="Stream",
        study_form_short_name="Full",
        achieves_count=0,
        registration_date=datetime(2024, 1, 1),
        last_date_visit=datetime(2024, 1, 1),
    )


def test_photo_url_none_when_missing() -> None:
    assert _user().photo_url is None


def test_photo_url_str_when_present() -> None:
    user = _user(photo=HttpUrl("https://example.com/photo.png"))
    assert user.photo_url == "https://example.com/photo.png"


def test_gaming_points_totals() -> None:
    user = _user()
    assert user.top_coins == 10
    assert user.top_gems == 3
    assert user.total_gaming_points == 13


def test_gaming_points_empty() -> None:
    user = _user()
    user.gaming_points = []
    assert user.top_coins == 0
    assert user.top_gems == 0


def test_gaming_point_type_name() -> None:
    user = _user()
    by_type = {gp.new_gaming_point_types__id: gp.type_name for gp in user.gaming_points}
    assert by_type[GamingPointType.TOP_COINS] == "Топ коины"
    assert by_type[GamingPointType.TOP_GEMS] == "Топ гемы"
