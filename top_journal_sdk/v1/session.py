class SessionContext:
    """
    Контекст сессии залогиненного пользователя.

    Logged-in user session context.

    Единый изменяемый объект, разделяемый между SDK и контроллерами:
    login() заполняет его из user-info, контроллеры читают значения
    по умолчанию (например group_id) через резолверы BaseController.
    """

    def __init__(self) -> None:
        self.group_id: int | None = None
        self.student_id: int | None = None
