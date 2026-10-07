"""Проверяет, что дедуплицированные DTO валидируются так же, как раньше."""

from top_journal_sdk.models.attendance import AttendanceResponse
from top_journal_sdk.models.grades import GradeResponse
from top_journal_sdk.models.leaderboard import (
    GroupLeaderboardResponse,
    StreamLeaderboardResponse,
)


def test_grade_response_matches_attendance_shape() -> None:
    payload = {
        "date": "2024-05-01",
        "points": 5,
        "previous_points": 4,
        "has_rasp": True,
    }
    grade = GradeResponse.model_validate(payload)
    attendance = AttendanceResponse.model_validate(payload)
    assert isinstance(grade, AttendanceResponse)
    assert grade.model_dump() == attendance.model_dump()


def test_stream_leaderboard_matches_group_shape() -> None:
    payload = {
        "amount": 100,
        "id": 1,
        "full_name": "Test Student",
        "photo_path": None,
        "position": 2,
    }
    stream = StreamLeaderboardResponse.model_validate(payload)
    group = GroupLeaderboardResponse.model_validate(payload)
    assert isinstance(stream, GroupLeaderboardResponse)
    assert stream.model_dump() == group.model_dump()
