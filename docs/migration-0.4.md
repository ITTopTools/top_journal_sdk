# Migration from 0.3 to 0.4

Python 3.13 or newer is required. `TopJournalSDK` continues to target API v1;
upgrading the package does not automatically switch existing code to journalka.

## Imports

These imports remain available:

```python
from top_journal_sdk import DEFAULT_TIMEOUT, SessionContext, TopJournalSDK
```

Version-specific modules moved into `v1`; old module paths are not aliases:

| 0.3 | 0.4 |
|---|---|
| `top_journal_sdk.models.*` | `top_journal_sdk.v1.models.*` |
| `top_journal_sdk.controllers.*` | `top_journal_sdk.v1.controllers.*` |
| `top_journal_sdk.exceptions` | `top_journal_sdk.v1.exceptions` |
| `top_journal_sdk.enums.*` | `top_journal_sdk.v1.enums.*` |
| `top_journal_sdk.session` | `top_journal_sdk.v1.session` |
| `top_journal_sdk.rapid.client` | `top_journal_sdk.v1.rapid.client` |
| `top_journal_sdk.utils.app_key` | `top_journal_sdk.v1.utils.app_key` |

Import auxiliary classes from their version-specific modules, including classes
that happened to be re-exported by the old root module:

```python
from top_journal_sdk.v1.exceptions import JournalException
from top_journal_sdk.v1.models.auth import LoginRequest
```

## The new v2 client

```python
from top_journal_sdk import TopJournalSDKV2
```

V1 and v2 have separate HTTP clients and authorization state. V1 uses Bearer
JWTs and domain exceptions; v2 uses cookies and `httpx.HTTPStatusError`.
V2 currently has auth, user, dashboard and profile controllers; it does not
provide all v1 controllers. Switching clients requires adapting API calls.

V2 is new in the 0.4 release. If you used an earlier repository preview,
[model contracts](models.md) describe the updated return types and reminder methods.

## Browser support

The base install does not include Playwright:

```bash
pip install 'top-journal-sdk[browser]==0.4.0'
playwright install chromium
```

Browser fallback is enabled by default, but is used only on supported access
blocks/challenges or connection-establishment failures. A missing browser raises
an installation error when fallback is needed. Disable it with
`TopJournalSDK(browser_fallback=False)` or `TopJournalSDKV2(auto_refresh_ddg=False)`.
A browser can still be denied access by DDoS-Guard.

## Response data and sessions

Additional fields are now preserved, so serialized responses may contain more
keys than before. `model_dump(exclude_unset=True, mode="json", by_alias=True)`
includes only received fields, using JSON representations of known types.
Partially known schemas are documented explicitly and preserve additional JSON.

After closing and reopening v1, log in again: its old refresh token and user/group
context are cleared. A successful v2 logout removes authentication cookies.
