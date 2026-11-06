from __future__ import annotations

from top_journal_sdk.v2.models._base import V2Model


class StoryItem(V2Model):
    id: int
    title: str
    thumbnail_url: str
    media_url: str
    link_url: str
    media_type: str
    duration: int
    muted: bool
    sort_index: int


class StoriesResponse(V2Model):
    items: list[StoryItem]


class StoryLeadResponse(V2Model):
    id: int | None = None
    title: str | None = None
    thumbnail_url: str | None = None
    media_url: str | None = None
    link_url: str | None = None
    media_type: str | None = None
    duration: int | None = None
    muted: bool | None = None
    sort_index: int | None = None
