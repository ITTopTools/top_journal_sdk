import datetime

from pydantic import BaseModel, HttpUrl


class LibraryAccessibilityResponse(BaseModel):
    """Доступность материала библиотеки.

    Library material accessibility.
    """

    response_code: int | None = None
    last_check: datetime.datetime | None = None


class LibraryMaterialResponse(BaseModel):
    """Материал библиотеки.

    Library material.
    """

    filename: str | None = None
    url: HttpUrl | None = None
    download_url: HttpUrl | None = None
    accessibility: LibraryAccessibilityResponse | None = None
    cover_image: HttpUrl | None = None
    material_content_id_from_editor: int | None = None
    description: str | None = None
    material_id: int | None = None
    theme: str | None = None
    current_week: int | None = None
    public_week: int | None = None
    material_type: int | None = None
    id_spec: int | None = None
    name_spec: str | None = None
    subject_source: int | None = None
    subject_id: int | None = None
    public_week_id: int | None = None
    is_new_material: bool | None = None
    date: datetime.datetime | None = None
    sort_date: int | None = None


class LibraryMaterialsResponse(BaseModel):
    library_material_list: list[LibraryMaterialResponse]


class LibraryCountResponse(BaseModel):
    """Счетчик материалов библиотеки.

    Library materials counter.
    """

    material_type_id: int
    materials_count: int
    new_count: int
    recommended_count: int


class LibraryCountsResponse(BaseModel):
    library_count_list: list[LibraryCountResponse]
