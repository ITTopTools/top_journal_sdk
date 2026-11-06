from __future__ import annotations

from top_journal_sdk.v2.models._base import V2Model


class HomeworkStatsResponse(V2Model):
    homework_total: int
    homework_new: int


class MaterialsStatsResponse(V2Model):
    materials_total: int


class PageCountersResponse(V2Model):
    announcements_unread: int
    reviews_unread: int
    materials_new: int
    vacancy_unread: int
    signal_unread: int
    profile_unread: int


class SupportStatsResponse(V2Model):
    support_unread: int
