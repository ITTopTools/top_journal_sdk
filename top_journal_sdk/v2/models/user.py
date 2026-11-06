from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from top_journal_sdk.v2.models._aliases import to_camel


class Group(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    id: int
    name: str
    group_status: int = 0
    is_primary: bool = False


class VisibilitySettings(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    is_design: bool = False
    is_video_courses: bool = False
    is_vacancy: bool = False
    is_signal: bool = False
    is_promo: bool = False
    is_test: bool = False
    is_email_verified: bool = False
    is_quizzes_expired: bool = False
    is_debtor: bool = False
    is_phone_verified: bool = False
    is_only_profile: bool = False
    is_referral_program: bool = False
    is_dz_group_issue: bool = False
    is_birthday: bool = False
    is_school: bool = False
    is_news_popup: bool = False
    is_school_branch: bool = False
    is_college_branch: bool = False
    is_higher_education_branch: bool = False
    is_russian_branch: bool = False
    is_academy_branch: bool = False
    is_shambala_college: bool = False


class User(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    id: int
    full_name: str
    group_name: str
    current_group_id: int
    groups: list[Group]
    stream_name: str
    avatar: str | None = None
    level: int = 0
    top_coin: int = 0
    top_gem: int = 0
    top_money: int = 0
    spent_top_coin: int = 0
    spent_top_gem: int = 0
    current_top_coin: int = 0
    current_top_gem: int = 0
    point_scale: int = 0
    visibility_settings: VisibilitySettings | None = None


class UserInfoResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    user: User
