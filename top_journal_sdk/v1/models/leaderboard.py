from pydantic import HttpUrl

from top_journal_sdk._models import APIModel


class GroupLeaderboardResponse(APIModel):
    amount: int
    id: int
    full_name: str
    photo_path: HttpUrl | None
    position: int


class GroupLeaderboardsResponse(APIModel):
    group_leaderboard_list: list[GroupLeaderboardResponse]


class StreamLeaderboardResponse(GroupLeaderboardResponse):
    """Запись рейтинга потока.

    Тот же набор полей, что и у рейтинга группы
    (amount/id/full_name/photo_path/position).
    """

    pass


class StreamLeaderboardsResponse(APIModel):
    stream_leaderboard_list: list[StreamLeaderboardResponse]
