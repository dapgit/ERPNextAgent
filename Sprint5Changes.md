# Sprint 5 Changes — ERPNext REST Integration

Objective: replace the mock data source with a real ERPNext backend without changing the Tool or Service layers.

## Milestone 5.1 — Client Foundation

**Goal:** introduce a dedicated Client layer so Repositories deal in business entities and the Client deals in HTTP.

- `settings.py` — added `get_erpnext_url()`, `get_erpnext_api_key()`, `get_erpnext_api_secret()` so the rest of the app never reads `os.environ` directly.
- `.env` / `.env.example` — added `ERPNEXT_URL`, `ERPNEXT_API_KEY`, `ERPNEXT_API_SECRET`.
- `clients/erpnext_client.py` (new) — `ERPNextClient` with a `get()` method: builds URLs, sets the `Authorization: token <key>:<secret>` header, does the GET, parses JSON.
- `utils/exceptions.py` (new) — `ERPNextClientError` base with `ERPNextConnectionError`, `ERPNextAuthenticationError`, `ERPNextResponseError`.
- `requirements.txt` — added `requests`.
- Removed `services/erpnext_client.py` — an empty, unreferenced stub left over from an earlier sprint, superseded by `clients/`.

## Milestone 5.2 — Session Reuse + Independent Connectivity Check

**Goal:** confirm the client alone can reach ERPNext and retrieve Company data, before involving Repository/Service.

- `clients/erpnext_client.py` — switched from a per-request `requests.get()` call to a `requests.Session()` created once in `__init__`, with auth headers set once instead of rebuilt per call. Added `close()` / `__enter__` / `__exit__` for cleanup. Public interface (`get(path, params)`) unchanged.
- `tests/test_erpnext_client.py` (new) — one test verifies session/header reuse without hitting the network; one test calls the live ERPNext instance through `ERPNextClient` only (no Repository/Service) and confirms Company data comes back. Skips gracefully if `ERPNEXT_URL` isn't configured or the server is unreachable.
- Verified live against `http://localhost:8080`: retrieved real companies (`A Sports`, `A Sports (Demo)`), confirming connectivity and authentication both work.
- Noted for later: ERPNext's `Company` doctype has no `fiscal_year` or `industry` field, unlike the mock `Company` model.

## Milestone 5.3 — Replace the Company Repository

**Goal:** make the Company repository the first real consumer of the client, following review feedback, while keeping Tool/Service untouched.

- Renamed `clients/erpnext_client.py` → `clients/erpnext_rest_client.py`, class `ERPNextClient` → `ERPNextRESTClient` (leaves room for a future `ERPNextMCPClient` sharing the same repository contract).
- `clients/erpnext_rest_client.py` — added `get_doc(doctype, name)` and `get_list(doctype, fields, filters)` to centralize URL construction; repositories no longer hand-build `/api/resource/...` paths.
- `utils/exceptions.py` — expanded hierarchy: `ERPNextError` (renamed from `ERPNextClientError`) with `ERPNextConnectionError`, `ERPNextTimeoutError`, `ERPNextAuthenticationError`, `ERPNextResourceNotFoundError`, `ERPNextValidationError`, `ERPNextResponseError`. The client now maps HTTP status codes (401/403, 404, 400/417, timeout) to the specific exception.
- `settings.py` — added `get_erpnext_company_name()`; `.env` / `.env.example` gained `ERPNEXT_COMPANY` (optional — falls back to the first company visible to the API user if unset).
- `repositories/company_repository.py` — rewritten:
  - `CompanyRepository(ABC)` with abstract `get_company_information()`.
  - `MockCompanyRepository` — the original in-memory data, now behind the interface.
  - `ERPNextCompanyRepository(client=None, company_name=None)` — constructor-injected client (defaults to a real `ERPNextRESTClient()` if not given), fetches the Company document, and maps ERPNext JSON to the `Company` dataclass. `fiscal_year`/`industry` default to `"Not tracked on Company in ERPNext"` since those fields don't exist on ERPNext's Company doctype.
  - Module-level `get_company_information()` factory: picks `ERPNextCompanyRepository` if `ERPNEXT_URL` is configured, else `MockCompanyRepository`. This is what let `services/company_service.py` stay byte-for-byte unchanged.
- `tests/test_erpnext_rest_client.py` (renamed from `test_erpnext_client.py`) — updated for the new class name; added a URL-building test.
- `tests/test_company_repository.py` (new) — uses a fake client (no network) to verify the ABC contract, JSON→domain mapping, and the first-company fallback.

**Verified end-to-end:**
- `git diff --stat` on `services/company_service.py`, `tools/company.py`, `models/company.py` — zero diff.
- `python3 app.py` → "Tell me about our company" now returns real ERPNext data (`A Sports`, India, INR) instead of the `ABC Traders Pvt Ltd` mock.
- Full test suite: 7 passed.

## Not yet done

- Customer, Item, and Supplier repositories still return mock data — same ABC + Mock/ERPNext pattern applies when those are tackled.
- No resolution yet for `fiscal_year`/`industry` not existing on ERPNext's Company doctype (currently a placeholder string).
- No retry/backoff, logging, or write operations (POST/PUT/DELETE) — out of scope for Sprint 5 per the "keep it intentionally small" direction.
