from top_journal_sdk._models import APIModel


class SpecModel(APIModel):
    """Предмет (специальность).

    Subject (spec).

    Используется в design-specs портфолио и public-specs настроек.
    """

    id: int
    name: str | None = None
    short_name: str | None = None
    subject_source: int | None = None
    subject_id: int | None = None


class SpecsResponse(APIModel):
    spec_list: list[SpecModel]
