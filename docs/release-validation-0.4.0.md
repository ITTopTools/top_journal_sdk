# Validation record: 0.4.0

Checked on 2026-11-07. Publication has not been performed.

## Distribution installation matrix

All checks ran from `/tmp` with fresh virtual environments. `python -I` and
pytest's `--import-mode=importlib` ensured imports came from installed artifacts,
not the checkout. The smoke script explicitly asserts the installed module path.

| Python | Artifact | Browser extra | Offline suite | Distribution smoke |
|---|---|---|---|---|
| 3.13.14 | wheel | absent | 524 passed, 3 skipped | passed |
| 3.14.6 | wheel | present | 527 passed | passed |
| 3.13.14 | sdist | absent | 524 passed, 3 skipped | passed |
| 3.14.6 | sdist | present | 527 passed | passed |

The three skips require optional Playwright. In all four runs the 27 live tests
were excluded by the default marker selection. Registry installation resolved
Pydantic 2.14.3, httpx 0.28.1 and rapid-api-client 0.10.0; the browser environment
also installed Playwright 1.64.1. `uv pip check` passed in both environments.
Browser installation, imports and mocked recovery were checked; these runs did
not exercise a live browser challenge against the journal.

## Migration and typing

- Installed the existing local 0.3.0 wheel in the Python 3.13 environment and
  checked the original root SDK imports and client initialization.
- Upgraded that installation to the 0.4.0 sdist and repeated the distribution
  smoke and offline suite successfully. Required import-path changes are listed
  in [migration](migration-0.4.md); old version-specific paths are not retained.
- Added the missing `py.typed` marker and checked it in installed wheel and sdist.
- An external Pyright check against the installed Python 3.14 package confirmed
  concrete return types for attendance, dates and document fields.

## Build and source checks

- Source suite: 527 passed, 27 live tests excluded.
- Ruff lint and formatting, ty and Pyright: passed.
- Wheel built through the source distribution: passed.
- `twine check --strict` for both 0.4.0 artifacts: passed.
- Pytest fixture loop scope is explicitly `function`, removing the warning seen
  with the fresh pytest-asyncio version.

The final artifacts are `dist/top_journal_sdk-0.4.0-py3-none-any.whl` and
`dist/top_journal_sdk-0.4.0.tar.gz`. Their final local checksums are written to
`dist/SHA256SUMS-0.4.0` after the release-preparation commit is built. Artifacts
and checksums are local build outputs and are not committed.

## Registry and remaining release steps

On the check date, the [PyPI registry metadata](https://pypi.org/pypi/top-journal-sdk/json)
reported version 0.3.0; the 0.4.0 version endpoint returned 404.

No tag, GitHub release or PyPI upload was created. The changelog remains
Unreleased until publication is approved. Publication credentials/trusted
publisher configuration have not been verified.

Live API tests were not repeated as part of these packaging checks. Earlier
v2 live validation passed all 13 cases, one after a retry; v1 remains limited by
DDoS-Guard from this environment. These results do not establish access from all
IPs or complete schemas for endpoints returning empty lists.

Follow [release preparation](release-0.4.0.md) for final publication steps.
