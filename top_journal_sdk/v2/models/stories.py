from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from top_journal_sdk.v2.models._aliases import to_camel


class StoryItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    id: int
    title: str
    thumbnail_url: str
    media_url: str
    link_url: str
    media_type: str
    duration: int
    muted: bool
    sort_index: int


class StoriesResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    items: list[StoryItem]


class StoryLeadResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    id: int | None = None
    title: str | None = None
    thumbnail_url: str | None = None
    media_url: str | None = None
    link_url: str | None = None
    media_type: str | None = None
    duration: int | None = None
    muted: bool | None = None
    sort_index: int | None = None
