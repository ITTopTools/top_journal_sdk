from pydantic import BaseModel


class TeacherContactResponse(BaseModel):
    """Контакт преподавателя.

    Teacher contact.

    Точная форма пока не подтверждена: для тестового аккаунта список пуст.
    Модель будет уточнена по первому непустому образцу.
    """


class ContactsResponse(BaseModel):
    """Контакты филиала.

    Branch contacts.

    Все поля опциональны: состав зависит от филиала.
    """

    adress: str | None = None
    learning_tel: str | None = None
    teach_main: str | None = None
    href_teach: str | None = None
    tel_room: str | None = None
    tel_book: str | None = None
    tel_economists: str | None = None
    site_shag: str | None = None
    mail_shag: str | None = None
    vk: str | None = None
    facebook: str | None = None
    instagram: str | None = None
    youtube: str | None = None
    twitter: str | None = None
    google_maps: str | None = None
    google_plus: str | None = None
    teach_contacts: list[TeacherContactResponse] | None = None
    schedule_academic: str | None = None
    schedule_office: str | None = None
    remote_class_address: str | None = None
    happy_manager_contacts: list[TeacherContactResponse] | None = None
