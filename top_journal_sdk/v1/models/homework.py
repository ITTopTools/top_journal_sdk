from datetime import date, datetime
from enum import IntEnum

from pydantic import HttpUrl

from top_journal_sdk._models import APIModel
from top_journal_sdk.v1.exceptions import DataNotFoundError


class HomeworkCounterType(IntEnum):
    OVERDUE = 0
    CHECKED = 1
    PENDING = 2
    CURRENT = 3
    TOTAL = 4
    DELETED = 5


class HomeworkCounterResponse(APIModel):
    counter_type: HomeworkCounterType
    counter: int


class HomeworksResponse(APIModel):
    counter_list: list[HomeworkCounterResponse]

    def get_counter(self, counter_type: int | HomeworkCounterType) -> int:
        if isinstance(counter_type, HomeworkCounterType):
            counter_type = counter_type.value

        for counter in self.counter_list:
            if counter.counter_type == counter_type:
                return counter.counter
        raise DataNotFoundError(message=f"Homework counter {counter_type} not found")

    @property
    def overdue(self) -> int:
        return self.get_counter(HomeworkCounterType.OVERDUE)

    @property
    def checked(self) -> int:
        return self.get_counter(HomeworkCounterType.CHECKED)

    @property
    def pending(self) -> int:
        return self.get_counter(HomeworkCounterType.PENDING)

    @property
    def current(self) -> int:
        return self.get_counter(HomeworkCounterType.CURRENT)

    @property
    def total(self) -> int:
        return self.get_counter(HomeworkCounterType.TOTAL)

    @property
    def deleted(self) -> int:
        return self.get_counter(HomeworkCounterType.DELETED)


class HomeworkSubmissionResponse(APIModel):
    """Сданная работа студента.

    Submitted student work.
    """

    id: int
    filename: str | None = None
    file_path: HttpUrl | None = None
    tmp_file: str | None = None
    mark: int | None = None
    creation_time: datetime | None = None
    stud_answer: str | None = None
    auto_mark: bool | None = None


class HomeworkCommentResponse(APIModel):
    """Комментарий к домашнему заданию.

    Homework assignment comment.
    """

    text_comment: str | None = None
    attachment: str | None = None
    attachment_path: str | None = None
    date_updated: datetime | None = None


class HomeworkListItemResponse(APIModel):
    """Запись списка домашних заданий.

    Homework list entry.
    """

    id: int
    id_spec: int
    subject_source: int
    subject_id: int
    id_teach: int
    id_group: int
    fio_teach: str | None = None
    theme: str | None = None
    completion_time: date | None = None
    creation_time: date | None = None
    overdue_time: date | None = None
    filename: str | None = None
    file_path: HttpUrl | None = None
    comment: str | None = None
    name_spec: str | None = None
    status: int | None = None
    common_status: int | None = None
    homework_stud: HomeworkSubmissionResponse | None = None
    homework_comment: HomeworkCommentResponse | None = None
    cover_image: str | None = None


class HomeworksListResponse(APIModel):
    homework_list: list[HomeworkListItemResponse]


class HomeworkTagResponse(APIModel):
    """Тег оценки домашнего задания.

    Homework evaluation tag.
    """

    id: int
    translate_key: str
    type: str


class HomeworkTagsResponse(APIModel):
    homework_tag_list: list[HomeworkTagResponse]


class GroupHistorySpecResponse(APIModel):
    """Предмет в истории группы.

    Subject in group history.
    """

    id: int
    name: str
    short_name: str | None = None
    subject_source: int | None = None
    subject_id: int | None = None


class GroupHistoryResponse(APIModel):
    """Запись истории группы по домашним заданиям.

    Homework group history entry.
    """

    specs: list[GroupHistorySpecResponse]
    id: int
    name: str


class GroupHistoriesResponse(APIModel):
    group_history_list: list[GroupHistoryResponse]
