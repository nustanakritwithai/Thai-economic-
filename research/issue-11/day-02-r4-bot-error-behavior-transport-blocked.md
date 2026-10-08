# Issue #11 — Day 02 / R4: BOT Negative/Error Behavior — Transport-Blocked Evidence

**Project:** Thailand Economic OS
**Active Release:** V0.2 Core Data Connectors
**Current Issue:** #11 (OPEN)
**Research date:** 2026-10-08, Asia/Bangkok (Day-2 calendar plan 2026-10-09 remains advisory)
**Round:** R4 — Negative/Error Behavior
**Round execution state:** `RECORDED_WITH_TRANSPORT_BLOCKER`
**Provider HTTP error-behavior evidence:** `BLOCKED_NO_HTTP_RESPONSE` — NOT PASS
**R3 live positive auth:** remains `BLOCKED` under `BOT-R3-CRED-01`
**R5:** NOT STARTED
**Day-02 Gate:** NOT ASSESSED
**Production connector:** HOLD
**Day-01 Frozen v1.1:** unchanged.

## 1. QUESTION

For a minimal safe set of requests, how does the **current BOT Statistics Gateway actually behave** when Authorization is missing/invalid, paths/methods/parameters are invalid, or permissions are inadequate? Which observations distinguish **local transport failure** from HTTP/auth/permission/server errors?

The objective is **measured** behavior, not the generic convention that missing auth `→401`, forbidden `→403`, throttle `→429`, or unknown route `→404`. None of those mappings can be asserted without a provider response or official specific contract.

## 2. METHOD / SAFETY BOUNDARY

1. Recover Day-01 Frozen v1.1, R1/R2 and R3 scoped blocker; verify R4 is the active round.
2. Re-check **official BOT** Manual, Migration Guide, Statistics Product, Stat Category specification, and Terms of Use; read documented header and candidate route.
3. Choose the smallest **read-only** negative test: one `GET` with **no Authorization header** to a route assembled from BOT Statistics Stat Category's documented `https://gateway.api.bot.or.th/categorylist` base and displayed `/category_list/get` operation. Full method/contract is not independently proven due dynamic spec; route remains a **candidate** not a verified successful endpoint.
4. Attempt the one request with curl, **4-second connection timeout / 8-second total timeout**, no credential, no retries, no redirect following, no rate stress.
5. Distinguish DNS/transport tool errors from origin HTTP response. Abort additional negative tests after DNS failure, rather than generating meaningless invalid-token/method probes.
6. No secret access, BOT login, production code, parser, normalization, DB, forecast, or credential testing.

This work uses actual local execution diagnostics plus current BOT-source contracts, but **did not obtain an HTTP response from BOT**. The local execution environment's ability to resolve public domains is not a measure of BOT availability.

## 3. OFFICIAL BOT SOURCES / AUTHORITY SCOPE

| ID | Official BOT URL | Supported R4 fact / limit |
|---|---|---|
| R4-E01 | https://portal.api.bot.or.th/manual | Account/product approval precedes token; example header `Authorization`; BOT's screenshot has example 200, **not observed by Thailand OS**; Dashboard offers error-breakdown views but no measured error mapping here |
| R4-E02 | https://portal.api.bot.or.th/migration | New gateway `https://gateway.api.bot.or.th/`, new header `Authorization`; legacy `X-IBM-Client-Id` not current |
| R4-E03 | https://portal.api.bot.or.th/portal/catalogue-products/statistics-1 | Statistics Product has `/categorylist`, `/search-series`, `/observations`; plan display is not enforcement proof |
| R4-E04 | https://portal.api.bot.or.th/portal/catalogue-products/statistics-1/d48f73217fdf41995a38859ed2b6e2d5/docs | BOT indexed spec: Stat Category v1.0.0; **base URL** `https://gateway.api.bot.or.th/categorylist`, operation labels `/category_list/get`, `/series_list/get`; token specified for `Authorization`. Direct page extraction exposes only a dynamic HTML shell; exact HTTP operation contract not independently saved |
| R4-E05 | https://portal.api.bot.or.th/terms | Terms §5 prohibits interference/disruption, §6 protects access secrets; this R4 test was bounded to one normal read-only attempt |
| R4-E06 | https://portal.api.bot.or.th/ | Current portal/gateway identity (effective platform since September 2025) |

**Official-source retrieval/recheck date:** 2026-10-08. These are URL/date/claim references; immutable remote raw-page captures or raw OpenAPI exports are **not guaranteed**. Search-indexed BOT content is not equivalent to locally retained spec bytes.

## 4. LOCAL CONNECTION DIAGNOSTIC & ACTUAL REQUEST ATTEMPT

### R4-T00 — Ancillary portal domain diagnostic (not a BOT Gateway error test)

- Command intent: `curl --head` on public `https://portal.api.bot.or.th/migration`, with short timeouts.
- Outcome: `curl` exit **6**: `Could not resolve host: portal.api.bot.or.th`.
- Curl write-out `portal_http=000`, no remote IP, elapsed approximately 0.001255 s.
- Status: `LOCAL_DNS_RESOLUTION_FAILURE`. No origin HTTP response. `000` is **curl's no-response sentinel**, not a BOT HTTP status.

### R4-T01 — Missing Authorization on candidate Statistics route

**Candidate target assembled from official BOT base + displayed path (not verified operation):**
`https://gateway.api.bot.or.th/categorylist/category_list/get`

**Method:** `GET` (read-only test selection; published exact HTTP method not independently proven).
**Authorization header:** ABSENT.
**Attempted at:** `2026-10-08T10:30:29Z`.

Actual local diagnostic (sanitized; no credential was available or sent):

~~~text
method=GET
url=https://gateway.api.bot.or.th/categorylist/category_list/get
authorization_header=ABSENT
curl_exit_code=6
curl: (6) Could not resolve host: gateway.api.bot.or.th
http_code=000 remote_ip= total_seconds=0.000095 ssl_verify=0 redirect_url=
~~~

**Interpretation:**
- DNS failed in the current execution environment **before connecting** to BOT.
- No TLS session or HTTP response; no authenticated or unauthenticated BOT Gateway HTTP status observed.
- `http_code=000` is a local `curl` placeholder. `ssl_verify=0` at this stage does **not** mean BOT TLS was verified (TLS did not occur).
- `total_seconds` is local failed-attempt timing, **not** BOT request latency.
- Origin `status`, response headers, response body, `Content-Type`, `Retry-After`, and `retrieved_at` are all `null/NOT_OBSERVED`.
- No evidence that BOT is down, rejects a missing token, returns 401, or responds with any other status.

### R4-T02 — Web-reader fetch attempt (tool capability check only)

A separate public web reader could not access the same gateway candidate URL. It returned a **tool access error**, not validated origin HTTP status/headers/body. It is **not an independent confirmation of a BOT error code**. Do not count this as an HTTP gateway response.

## 5. R4 SAFE NEGATIVE MATRIX — TRUTHFUL RESULTS

| Test case | Planned safe method | Actual disposition | Origin HTTP status | Why |
|---|---|---|---|---|
| Missing `Authorization` | One read-only GET to Stat Category candidate | **TRANSPORT BLOCKED**; local curl DNS exit 6 | `null` | No domain resolution, request never reached gateway |
| Malformed `Authorization` | One read-only request with known dummy placeholder only, no real token | **NOT EXECUTED** | `null` | DNS precondition failed; avoid pointless requests |
| Invalid credential | One read-only request with controlled non-secret invalid value | **NOT EXECUTED** | `null` | Same DNS failure; no rate/throttle probing |
| Invalid route | One harmless GET to clearly nonexistent path, only after valid transport | **NOT EXECUTED** | `null` | No HTTP access established |
| Unsupported method | Safe `HEAD` or `OPTIONS` if allowed, never mutating request | **NOT EXECUTED** | `null` | Transport prerequisite unfulfilled; operation method not independently confirmed |
| Invalid parameter | One invalid *known* parameter after exact spec inspection | **NOT EXECUTED** | `null` | Exact accepted parameter contract not captured, plus DNS failure |
| Insufficient product permission | Only naturally observed using legitimate authorized credential and a known mismatched access case | **BLOCKED** | `null` | No legitimate token/application entitlement in this execution context; R3 blocker remains open |

**Total actual gateway connection attempts from local curl:** 1.
**Total completed HTTP exchanges with BOT Gateway:** **0**.
**Total observed BOT HTTP statuses:** **0**.
**Forbidden inference:** 400/401/403/404/405/429/5xx statuses from customary REST mappings.

## 6. EVIDENCE-BASED CLASSIFICATION CONTRACT — RESEARCH ONLY

A future connector/error classifier must separate **observation** from **hypothesis**:

| Distinct layer | Example diagnostic evidence | R4 BOT-specific evidence |
|---|---|---|
| Local DNS / egress | Resolver failure before TCP/TLS/HTTP | **OBSERVED LOCALLY** — curl exit 6, NOT a BOT HTTP error |
| TLS / TCP / timeout | Local TLS/network exception before HTTP | NOT OBSERVED |
| Missing / bad authentication | Actual provider HTTP status, headers and safe error envelope | **UNKNOWN** |
| Authenticated but unauthorized product/scope | Valid token + actual permission failure response | **UNKNOWN** |
| Invalid path/method/parameter | Actual observed request/response pair | **UNKNOWN** |
| Throttling/quota | Actual HTTP and documented enforcement headers | **UNKNOWN**; BOT-U06 remains open |
| Maintenance/upstream/server | Official maintenance notice and/or actual HTTP evidence | **UNKNOWN at HTTP behavior scope** |
| Success (R3) | Valid token + actual BOT Statistics response | **BLOCKED**, not a synthetic 200 |

**Rules:** `transport_error` must never be assigned a provider `http_status`. If an HTTP response is observed later, record the **raw status as seen**, trusted response content type, bytes, allowlisted non-sensitive headers, exact method/path (no secrets), safe error-envelope summary and UTC observation timestamp. Do not infer authentication-vs-authorization-vs-throttle from number alone when BOT-specific mapping lacks direct evidence.

This is an **error taxonomy proposal**, not implemented code, not a verified BOT HTTP contract and not a V0.2 release-gate pass.

## 7. NEW SCOPED BLOCKER / RECOVERY TEST CONTRACT

**Blocker ID:** `BOT-R4-EGRESS-01`.
**Status:** OPEN — scoped only to R4 direct negative HTTP observation from current execution environment.
**Owner:** Research operator / authorized networking or runner administrator.
**Cause observed:** local DNS lookup failed for portal and gateway domains; no origin status measurable.
**Not established:** actual BOT outage, domain outage across the public Internet, API rejection or permission state.
**Impact:** R4 published error-status taxonomy cannot be validated using this runner. It does **not** block R5 documentation research.
**Workaround:** use official BOT documentation/Terms without promoting illustrative codes to live observations; preserve JSON `null` statuses.
**Resolution:** run a small, bounded set of read-only tests from an **authorized egress-enabled environment** able to resolve the gateway, after verifying operation/method details. Start with a single missing-Authorization test; record raw response. Only then consider harmless invalid/malformed credential/route cases, without stress tests. Do not expose or request any user secrets.
**Evidence handling:** retain this R4 report as an attempted blocked run; record later live R4 test as a new additive artifact/commit, never silently edit `null` to a claimed HTTP 401.

R3 blocker `BOT-R3-CRED-01` remains OPEN independently. An egress-enabled runner alone does not prove access approval; a valid approved token alone does not solve an egress failure. Both prerequisites have separate owners.

## 8. QUESTION → METHOD → EVIDENCE → FINDING → CONFIDENCE → UNKNOWN → IMPACT → NEXT QUESTION

**QUESTION:** Can real BOT missing/invalid-auth and other HTTP errors be identified now?
**METHOD:** current official source review; one short, unauthenticated read-only `curl GET`; stop after local DNS failure; classify additional tests as not executed.
**EVIDENCE:** R4-E01..E06; R4-T00 local portal DNS diagnostic; R4-T01 timestamped curl output; R4-T02 web-reader limitation.
**FINDING:** Documentation establishes gateway/header and candidate Stat Category endpoint; **no valid origin HTTP error status was measured**; only a local pre-HTTP DNS failure is empirically supported.
**CONFIDENCE:** HIGH for observed local curl exit 6 and 0 completed HTTP exchanges; HIGH for directly published portal/migration; MEDIUM for dynamically rendered/indexed route detail; **UNKNOWN** for provider HTTP behavior.
**UNKNOWN:** all HTTP statuses and response envelopes for auth, permission, invalid requests and throttling; `D2-AUTH-U07/U11` remain unresolved; `BOT-U06/U07` remain unresolved; all R3/BOT registers are preserved.
**IMPACT:** prevent false authentication error taxonomy; retain independently scoped egress and credential blockers. No implementation release.
**NEXT QUESTION:** Day 02 R5 — what **officially documented** product-plan quota, rate-limit scope, telemetry, retry signaling and maintenance/operational notices can be evidenced without rate-stress or a credential? Do not collapse documented plan into observed enforcement.

## 9. ROUND STOP POINT

- Day 1: **FROZEN v1.1 / GATE PASS** — unchanged.
- Day 2 R1/R2: recorded, revalidated (docs-only).
- Day 2 R3: live positive `BLOCKED` (`BOT-R3-CRED-01`).
- **Day 2 R4: `RECORDED_WITH_TRANSPORT_BLOCKER`, BOT negative HTTP tests `BLOCKED`, NOT PASS.**
- Day 2 R5–R8: NOT STARTED. Next research round R5 documentation/operations only.
- Issue #11: OPEN. Day-02 Gate: NOT ASSESSED. Production connector: HOLD.
- **UNKNOWN ≠ PASS.**
