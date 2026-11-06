from __future__ import annotations

import datetime as dt

from top_journal_sdk.v2.models._base import V2Model


class FutureExam(V2Model):
    """Date and subject consumed by the dashboard's future-exams renderer."""

    date: dt.date | dt.datetime
    spec: str


class AttendanceItem(V2Model):
    date: dt.date
    points: int


class AttendanceResponse(V2Model):
    items: list[AttendanceItem]


class ProgressItem(V2Model):
    date: dt.date
    points: int


class ProgressResponse(V2Model):
    items: list[ProgressItem]


class ActivityItem(V2Model):
    id: int
    date: dt.datetime
    title: str
    title_key: str
    points: int
    is_positive: bool
    point_type: int
    point_type_translate_key: str


class ActivityResponse(V2Model):
    items: list[ActivityItem]


class FutureExamsResponse(V2Model):
    items: list[FutureExam]


class LeaderboardItem(V2Model):
    id: int
    full_name: str
    photo_path: str | None = None
    position: int
    amount: int


class LeaderGroupResponse(V2Model):
    items: list[LeaderboardItem]


class LeaderGroupPointsResponse(V2Model):
    student_position: int
    total_students: int
    week_diff: int


class LeaderStreamResponse(V2Model):
    items: list[LeaderboardItem]


class LeaderStreamPointsResponse(V2Model):
    student_position: int
    total_students: int
    week_diff: int


class ReviewsCountResponse(V2Model):
    reviews_count: int


class AchievementsCountResponse(V2Model):
    active_achievements_count: int
