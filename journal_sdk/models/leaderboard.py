from pydantic import BaseModel, HttpUrl


class GroupLeaderboardResponse(BaseModel):
    amount: int
    id: int
    full_name: str
    photo_path: HttpUrl | None
    position: int


class GroupLeaderboardsResponse(BaseModel):
    group_leaderboard_list: list[GroupLeaderboardResponse]


class StreamLeaderboardResponse(BaseModel):
    id: int
    full_name: str
    photo_path: HttpUrl | None
    position: int
    amount: int


class StreamLeaderboardsResponse(BaseModel):
    stream_leaderboard_list: list[StreamLeaderboardResponse]
