from datetime import date

from pydantic import BaseModel, HttpUrl


class EvaluationTagResponse(BaseModel):
    id: int
    translate_key: str
    type: str


class EvaluationTagsResponse(BaseModel):
    evaluation_tags: list[EvaluationTagResponse]


class EvaluationResponse(BaseModel):
    key: str
    date_visit: date
    fio_teach: str
    spec_name: str
    teach_photo: HttpUrl | None


class EvaluationsResponse(BaseModel):
    evaluation_list: list[EvaluationResponse]


class EvaluationRequest(BaseModel):
    comment_lesson: str = ""
    comment_teach: str = ""
    key: str
    mark_lesson: int
    mark_teach: int
    tags_lesson: list[int]
    tags_teach: list[int]
