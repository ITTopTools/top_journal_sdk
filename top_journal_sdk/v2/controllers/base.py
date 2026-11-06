from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from top_journal_sdk.v2.client import TopJournalSDKV2


class BaseController:
    """Базовый контроллер с ссылкой на SDK v2."""

    def __init__(self, sdk: TopJournalSDKV2) -> None:
        self._sdk = sdk

    @property
    def sdk(self) -> TopJournalSDKV2:
        return self._sdk
