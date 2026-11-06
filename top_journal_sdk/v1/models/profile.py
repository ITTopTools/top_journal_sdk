import datetime

from pydantic import BaseModel, HttpUrl


class ProfilePhoneResponse(BaseModel):
    """Телефон профиля.

    Profile phone.
    """

    phone_type: int | None = None
    phone_number: str | None = None


class ProfileLinkResponse(BaseModel):
    """Ссылка профиля (соцсеть).

    Profile link (social network).
    """

    id: int | None = None
    name: str | None = None
    reg: str | None = None
    required_type: int | None = None
    value: str | None = None
    valid: bool | None = None
    is_required: bool | None = None


class ProfileRelativeResponse(BaseModel):
    """Родственник в профиле.

    Profile relative.

    Точная форма пока не подтверждена: для тестового аккаунта список пуст.
    Модель будет уточнена по первому непустому образцу.
    """


class ProfileAzureResponse(BaseModel):
    """Привязка Azure/Office в профиле.

    Azure/Office binding in profile.
    """

    login: str | None = None
    has_azure: bool | None = None
    has_office: bool | None = None


class ProfileSettingsResponse(BaseModel):
    """Настройки профиля студента.

    Student profile settings.
    """

    id: int | None = None
    ful_name: str | None = None
    address: str | None = None
    date_birth: datetime.date | None = None
    study: str | None = None
    email: str | None = None
    last_approving_status: int | None = None
    form_type: int | None = None
    photo_path: HttpUrl | None = None
    has_not_approved_data: bool | None = None
    has_not_approved_photo: bool | None = None
    is_email_verified: bool | None = None
    is_phone_verified: bool | None = None
    phones: list[ProfilePhoneResponse] = []
    links: list[ProfileLinkResponse] = []
    relatives: list[ProfileRelativeResponse] = []
    fill_percentage: int | None = None
    decline_comment: str | None = None
    azure: ProfileAzureResponse | None = None
    azure_login: str | None = None


class AchievementPointResponse(BaseModel):
    """Баллы достижения.

    Achievement points.
    """

    id: int
    points_count: int


class StudentAchievementResponse(BaseModel):
    """Достижение студента.

    Student achievement.
    """

    id: int
    translate_key: str | None = None
    is_active: bool | None = None
    achieve_points: list[AchievementPointResponse] = []


class StudentAchievementsResponse(BaseModel):
    student_achievement_list: list[StudentAchievementResponse]


class ProfileFormResponse(BaseModel):
    """Публичная форма настроек.

    Public settings form.
    """

    id: int
    form_name: str | None = None


class ProfileFormsResponse(BaseModel):
    profile_form_list: list[ProfileFormResponse]


class ChangeCurrentGroupRequest(BaseModel):
    """Смена текущей группы.

    Change current group.

    Поле по вызову фронта: идентификатор группы как `id_tgroups`.
    """

    id_tgroups: int
