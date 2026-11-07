# Release preparation: 0.4.0

Status: prepared locally; publication remains a separate step.

[Validation record dated 2026-11-07](release-validation-0.4.0.md).

## Release notes

0.4.0 adds the independent journalka v2 client and browser recovery for both API
versions. Response models preserve unknown JSON fields and validate confirmed
structures and temporal values. Session-refresh and lifecycle bugs are fixed.

**Migration required:** v1 modules moved into `top_journal_sdk.v1`; root imports
of `TopJournalSDK`, `DEFAULT_TIMEOUT` and `SessionContext` are retained. V2 is new
in this release and is not a drop-in replacement for the v1 controller surface.

- [Migration guide](migration-0.4.md)
- [Model contracts and partial schemas](models.md)
- [Changelog](../CHANGELOG.md)

DDoS-Guard can still deny headless browsers. Rare schemas remain partial, with
JSON preserved. Live tests do not perform mutating operations.

## Repeatable checks

Run from the checkout:

```bash
uv run pytest
uv run ruff check top_journal_sdk tests example.py
uv run ruff format --check top_journal_sdk tests example.py
uv run ty check top_journal_sdk tests example.py
uv run --with pyright pyright top_journal_sdk tests example.py
uv build
uvx twine check --strict dist/top_journal_sdk-0.4.0-py3-none-any.whl dist/top_journal_sdk-0.4.0.tar.gz
```

Do not upload `dist/*`: the directory can contain older release files.

For an isolated install, replace `/absolute/path/to/repo` below with the checkout
path. Run outside the checkout; `-I` prevents the source tree from hiding an
incomplete distribution. Check both Python 3.13 and 3.14, wheel and sdist, with
and without the browser extra in fresh environments.

```bash
uv venv --python 3.13 /tmp/top-journal-release-check
uv pip install --python /tmp/top-journal-release-check/bin/python /absolute/path/to/repo/dist/top_journal_sdk-0.4.0-py3-none-any.whl
cd /tmp
/tmp/top-journal-release-check/bin/python -I /absolute/path/to/repo/tests/distribution_smoke.py --expect-browser absent
```

The smoke check verifies the installed version and location, `py.typed`, all
module imports, retained root imports, model parsing and client cleanup. It
neither logs in nor makes network requests. To check the browser extra, install
`'/absolute/path/to/repo/dist/top_journal_sdk-0.4.0-py3-none-any.whl[browser]'`
and pass `--expect-browser present`. Chromium installation is a separate step.

## Publication gate

After approval to publish:

1. Review the final diff and clean worktree; mark the changelog release date.
2. Commit that change, rebuild artifacts from the final release commit and repeat
   package checks. Record SHA-256 hashes of those final files.
3. Create tag `v0.4.0` at that commit and push the commit and tag.
4. Publish GitHub release notes from the changelog and migration guide.
5. Upload only the two checked 0.4.0 files to PyPI, then verify installation from
   the registry. Registry credentials and publishing configuration are not checked
   by local preparation.

Do not change the release commit after building the files that will be uploaded.
