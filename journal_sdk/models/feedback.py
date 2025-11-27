from datetime import datetime

from pydantic import BaseModel


class ReviewResponse(BaseModel):
    date: datetime
    message: str
    spec: str
    full_spec: str
    teacher: str


class ReviewsResponse(BaseModel):
    review_list: list[ReviewResponse]
