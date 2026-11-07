"""Run with an installed wheel/sdist: python -I tests/distribution_smoke.py.

Uses no live credentials and makes no network requests. Run outside the checkout
with a fresh virtualenv so source files cannot hide missing distribution files.
"""

import argparse
import asyncio
import importlib
import importlib.util
import pkgutil
import sys
import tomllib
from importlib.metadata import distribution
from pathlib import Path

import top_journal_sdk
from top_journal_sdk import TopJournalSDK, TopJournalSDKV2
from top_journal_sdk.v1 import TopJournalSDK as V1Client
from top_journal_sdk.v1.models.dashboard import FutureExamResponse
from top_journal_sdk.v2 import TopJournalSDKV2 as V2Client
from top_journal_sdk.v2.models import AttendanceResponse, LessonEvaluationsResponse


async def check_clients() -> None:
    async with TopJournalSDK(browser_fallback=False) as sdk:
        assert sdk.auth is sdk.auth
        assert sdk.user is sdk.user
    async with TopJournalSDKV2(auto_refresh_ddg=False) as sdk:
        assert sdk.auth is sdk.auth
        assert sdk.client.is_closed is False
        client = sdk.client
    assert client.is_closed


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expect-browser", choices=("present", "absent"), default="absent")
    args = parser.parse_args()
    project_file = Path(__file__).resolve().parents[1] / "pyproject.toml"
    expected = tomllib.loads(project_file.read_text())["project"]["version"]
    dist = distribution("top-journal-sdk")
    assert dist.version == expected
    assert Path(top_journal_sdk.__file__).resolve().is_relative_to(Path(sys.prefix).resolve())
    assert Path(top_journal_sdk.__file__).with_name("py.typed").is_file()
    assert (importlib.util.find_spec("playwright") is not None) == (
        args.expect_browser == "present"
    )
    assert TopJournalSDK is V1Client
    assert TopJournalSDKV2 is V2Client
    for module in pkgutil.walk_packages(top_journal_sdk.__path__, "top_journal_sdk."):
        importlib.import_module(module.name)
    assert FutureExamResponse.model_validate({"newField": {"id": 1}}).model_dump() == {
        "newField": {"id": 1}
    }
    attendance = AttendanceResponse.model_validate(
        {"items": [{"date": "2026-11-07", "points": 5}]}
    )
    assert attendance.items[0].date.isoformat() == "2026-11-07"
    evaluations = LessonEvaluationsResponse.model_validate(
        {
            "items": [
                {
                    "key": "test",
                    "date_visit": "2026-11-07",
                    "fio_teach": "Teacher",
                    "spec_name": "Math",
                    "teach_photo": None,
                }
            ],
            "meta": {"requestedAt": "2026-11-07T10:00:00Z"},
        }
    )
    assert evaluations.items[0].spec_name == "Math"
    assert evaluations.meta.requested_at.year == 2026
    asyncio.run(check_clients())
    print(
        f"Distribution {dist.version}: Python {sys.version.split()[0]}, "
        f"browser={args.expect_browser}, imports/models/client lifecycle OK"
    )


if __name__ == "__main__":
    main()
