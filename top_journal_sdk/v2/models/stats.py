from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from top_journal_sdk.v2.models._aliases import to_camel


class HomeworkStatsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    homework_total: int
    homework_new: int


class MaterialsStatsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    materials_total: int


class PageCountersResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    announcements_unread: int
    reviews_unread: int
    materials_new: int
    vacancy_unread: int
    signal_unread: int
    profile_unread: int


class SupportStatsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    support_unread: int
