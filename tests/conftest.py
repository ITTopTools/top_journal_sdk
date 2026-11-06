"""Общая конфигурация pytest.

Подхватывает переменные из `.env` (если файл есть), чтобы live-тесты можно было
запускать командой `uv run pytest -m live` без ручного `export`.
"""

from __future__ import annotations

import os
from pathlib import Path

_ENV_PATH = Path(__file__).parent.parent / ".env"


def _load_env_file() -> None:
    if not _ENV_PATH.is_file():
        return
    for line in _ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        if key:
            os.environ.setdefault(key, value)


_load_env_file()
