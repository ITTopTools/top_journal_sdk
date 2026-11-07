# Changelog

## 0.4.0 — Unreleased

### Added

- `TopJournalSDKV2` for `journalka.top-academy.ru`: cookie authentication,
  automatic session refresh, dashboard and profile controllers.
- Optional Chromium fallback for blocked requests, including login, with session
  cookies transferred back to the HTTP client. Available to both API versions.
- Typed v2 responses, validated dates/times and preservation of additional JSON
  fields, including nested data and partially confirmed schemas.
- Synthetic contracts for all 165 public model classes and an installed-package
  smoke check in `tests/distribution_smoke.py`.
- PEP 561 `py.typed` marker in the wheel and source distribution.

### Changed

- **Breaking:** v1 modules moved under `top_journal_sdk.v1`. Root imports of
  `TopJournalSDK`, `DEFAULT_TIMEOUT` and `SessionContext` remain available.
- V2 controller responses use models and model lists. Consumers of repository
  previews should use attributes or `model_dump(mode="json")` instead of raw dicts.
- Reminder postponement uses POST; postponing an interview requires its ID.

### Fixed

- Loss of data in empty response models and unknown server fields.
- Cookie attribute loss, handling of failed refresh responses and concurrent
  token-refresh races.
- Stale session context after close, logout and failed profile loading during login.
- Object-valued startup prompts, moderation and profile rejection comments.
- Empty acknowledgements for group changes and reminder postponement.

### Known limitations

- DDoS-Guard may keep a headless browser on its verification page; browser fallback
  does not guarantee access from every IP. Live access to v1 remains unconfirmed
  from the development environment.
- Some rare schemas remain partial; their additional JSON fields are preserved
  and validated without claiming a complete domain schema.
- Mutating API operations are checked with mocks, not performed by live tests.

See [migration](docs/migration-0.4.md) and [model contracts](docs/models.md).
