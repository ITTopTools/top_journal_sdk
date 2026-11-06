from pydantic import BaseModel, HttpUrl


class GroupLeaderboardResponse(BaseModel):
    amount: int
    id: int
    full_name: str
    photo_path: HttpUrl | None
    position: int


class GroupLeaderboardsResponse(BaseModel):
    group_leaderboard_list: list[GroupLeaderboardResponse]


class StreamLeaderboardResponse(GroupLeaderboardResponse):
    """Запись рейтинга потока.

    Тот же набор полей, что и у рейтинга группы
    (amount/id/full_name/photo_path/position).
    """

    pass


class StreamLeaderboardsResponse(BaseModel):
    stream_leaderboard_list: list[StreamLeaderboardResponse]
