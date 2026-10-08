# Day-02 Gap #2 — Safe Single No-Token HTTP Candidate Probe

**Status:** PROBE HARNESS PREPARED; actual GitHub Actions evidence must be read after run.
**Active:** V0.2 / Issue #11 / Day-02 Frozen v1 with BLOCKED_CRITICAL_EVIDENCE gate.
**R3:** remains BLOCKED without an approved BOT Statistics credential.
**R4:** may gain one observed gateway-host HTTP response; no automatic full error-taxonomy PASS.

## Source / Endpoint Method Confidence

- Official BOT Statistics Product: https://portal.api.bot.or.th/portal/catalogue-products/statistics-1 lists Stat Category and /categorylist listen path.
- Official Stat Category v1.0.0 dynamically rendered documentation / indexed excerpt: https://portal.api.bot.or.th/portal/catalogue-products/statistics-1/d48f73217fdf41995a38859ed2b6e2d5/docs shows base https://gateway.api.bot.or.th/categorylist and an operation label /category_list/get, with API Key in Authorization.
- **GET is a safe read-only candidate, not verified from exported official raw OpenAPI bytes.** Direct public extraction exposes only dynamic shell, so full Method contract and extra parameters remain UNKNOWN (BOT-U07).
- Secondary community implementation: https://github.com/jwitmann/bankofthailand-go/blob/main/statistics.go uses GET for category list but calls a distinct suffix /category_list/; it is NOT an authoritative BOT spec and does not resolve path differences.
- Combined test URL (literal, no user inputs or query): https://gateway.api.bot.or.th/categorylist/category_list/get. This is constructed from official base and operation display, not yet proven live-successful.

## One-Shot Scope & Safety

- Use GitHub-hosted Linux Runner on main. The prior 2026-10-08 run 37796439277 confirmed this environment can complete BOT DNS/TCP/TLS, but each run has a new runner and no uptime claim.
- A single GET; no Authorization or other credential header, no body, no redirects, no automatic retries, no parameters, 7-second timeout. No parallel calls or rate stress. A network exception gives a null HTTP status.
- Python HTTPSConnection uses default CA and hostname checks. The GET target is fixed; public workflow provides no secrets and does not respond to pull requests.
- Record only HTTP status if observed, sanitized content-type (MIME alone), numeric Content-Length if present, presence (not values) of safe diagnostic response header names, local elapsed time and UTC observation. No response body, complete headers, cookies, Location values or error trace.
- A status at verified hostname may originate at edge/WAF/router or backend. HTTP 200 (especially text/html) cannot prove valid BOT API access; 401/403/404/429 cannot be mapped to BOT-specific semantics without official current spec and response-body evidence (excluded from this safe probe).
- A response at this candidate path is valuable evidence of reachable HTTP at official gateway hostname, not proof of all API operations or approved credentials.

## Expected Evidence and Outcome Gate

- Workflow & script: .github/workflows/bot-http-negative-diagnostic.yml and research/issue-11/diagnostics/bot_http_negative_probe.py
- Synthetic isolated tests: research/issue-11/diagnostics/test_bot_http_negative_probe.py (no real HTTP)
- Outputs: http-evidence.json, http-summary.md, GitHub log sanitized BOT_HTTP_NEGATIVE_EVIDENCE
- Zero observed status -> TRANSPORT/HTTP_PARSE_BLOCKED, not 401.
- Any observed status -> HTTP_RESPONSE_AT_BOT_GATEWAY_HOST_STATUS_UNINTERPRETED and no automatic R4 full PASS.
- No credential is ever loaded or disclosed.
- Preserve historical R4 local DNS failure and original Day-02 Frozen v1. New evidence must be additive.

## Next

Inspect the exact workflow run and CI for this Git commit. Update Issue #11 and Project State with actual evidence, not a predicted status; keep Day-02 gate BLOCKED_CRITICAL_EVIDENCE until positive authorization, verified official operation/method and sufficient BOT-specific behavior are proven.

UNKNOWN != PASS.
