from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict

from top_journal_sdk.v2.models._aliases import to_camel


class AttendanceItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    date: str
    points: int


class AttendanceResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    items: list[AttendanceItem]


class ProgressItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    date: str
    points: int


class ProgressResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    items: list[ProgressItem]


class ActivityItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    id: int
    date: str
    title: str
    title_key: str
    points: int
    is_positive: bool
    point_type: int
    point_type_translate_key: str


class ActivityResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    items: list[ActivityItem]


class FutureExamsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    items: list[dict[str, Any]]


class LeaderboardItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    id: int
    full_name: str
    photo_path: str | None = None
    position: int
    amount: int


class LeaderGroupResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    items: list[LeaderboardItem]


class LeaderGroupPointsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    student_position: int
    total_students: int
    week_diff: int


class LeaderStreamResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    items: list[LeaderboardItem]


class LeaderStreamPointsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    student_position: int
    total_students: int
    week_diff: int


class ReviewsCountResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    reviews_count: int


class AchievementsCountResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    active_achievements_count: int
