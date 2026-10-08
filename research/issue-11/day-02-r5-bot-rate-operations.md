# Issue #11 — Day 02 / R5: BOT Rate Limits and Operational Behavior Research

**Project:** Thailand Economic OS
**Active release:** V0.2 — Core Data Connectors
**Issue:** #11 — OPEN
**Research round:** Day 02 R5 — Rate Limit & Operational Behavior
**Research date:** 2026-10-08 (Asia/Bangkok; originally planned Day 02 calendar date 2026-10-09, calendar is not a gate)
**Status:** `DOCUMENTARY_RESEARCH_RECORDED_WITH_RUNTIME_UNKNOWNS`
**API rate enforcement PASS:** NOT ESTABLISHED
**Day-02 Gate:** NOT ASSESSED
**R3 Live Positive Auth:** BLOCKED (`BOT-R3-CRED-01`)
**R4 Live Negative/Error HTTP:** BLOCKED (`BOT-R4-EGRESS-01`)
**R6:** NOT STARTED
**Implementation:** HOLD
**Day-01 FROZEN v1.1:** unchanged

## 1. QUESTION

Which BOT **officially displayed** Product/Plan rate limits and quota definitions can be substantiated today? How are actual enforcement scope, HTTP rate/reset/retry signals, portal Dashboard telemetry, and maintenance announcements documented? Which apparent conflicts must be preserved without inventing live behavior?

No stress test, gateway probe, credential use, account login, parser, retry engine, connector, DB or rate limiter implementation is permitted in this research round.

## 2. METHOD

1. Read current repo NOW state and Day-02 R1–R4 evidence; confirm R3/R4 live proof blockers.
2. Independently inspect BOT-hosted **Statistics**, **Exchange Rates**, and **Interest Rates** Product/Plan pages, separately, for current `Quota`/`Rate` display.
3. Recheck BOT Manual §§3.7, 4.1–4.6 and the directly linked official illustration images for Application Product/Plan placement and Dashboard telemetry. Treat screenshot figures as **illustrative**, not measured usage.
4. Inspect BOT **Terms of use** for legally published service limitation and outage rights; inspect a dated official BOT API maintenance notice as an example of an official notification surface.
5. Target official-domain searches for `Retry-After`, `RateLimit-Remaining`, `RateLimit-Reset`, `X-RateLimit`, error responses, enforcement key/window, and maintenance status. **No authoritative current contract or real response with these values was found in inspected sources**; this is a scoped negative finding, **not proof that headers/functions do not exist**.
6. Record source authority, confidence, caveat, invalidation triggers and exact closure routes. No external page raw snapshot/checksum was established in this round.

**Credential / Gateway request count during R5:** 0. **BOT Gateway HTTP responses measured during R5:** 0. The prior R4 local DNS issue was **not retested**. A web reader's ability to read public portal HTML does not establish gateway egress or token-bearing runtime readiness.

## 3. PRIMARY OFFICIAL BOT EVIDENCE (2026-10-08)

| Evidence ID | Source | Authority / observation | Limit |
|---|---|---|---|
| R5-E01 | https://portal.api.bot.or.th/portal/catalogue-products/statistics-1 | Statistics Product: displayed plan `Quota: unlimited`, `Rate: 2000 calls / 1 hour(s)` | Displayed configuration only, not live enforcement |
| R5-E02 | https://portal.api.bot.or.th/portal/catalogue-products/exchange-rates-1 | Exchange Rates Product: unlimited quota, 200 calls / 1 hour(s) | Another product/plan, not the Statistics entitlement |
| R5-E03 | https://portal.api.bot.or.th/portal/catalogue-products/interest-rates-1 | Interest Rates Product: unlimited quota, 200 calls / 1 hour(s) | Another product/plan |
| R5-E04 | https://portal.api.bot.or.th/manual | §3.7 Product rate in app detail; §4 Dashboard → Performance; weekly view; CSV export; top five error rates and error breakdown | Published user guide, no real session observed |
| R5-E05 | https://portal.api.bot.or.th/assets/images/manual/Illustration%209.png | App/Approved Access screenshot shows Statistics Plan, unlimited quota, **1000 calls / 1 minute(s)** | Illustrative unversioned screenshot, conflicts with current Statistics listing |
| R5-E06 | https://portal.api.bot.or.th/assets/images/manual/Illustration%2011-1.png | Dashboard illustration: Performance Overview; total calls; error rate; latency; app filter; success/error graph; CSV | Example values are **not** measured project API traffic |
| R5-E07 | https://portal.api.bot.or.th/assets/images/manual/Illustration%2011-2.png | Dashboard illustration: Top 5 highest error rates by API; Error breakdown; an example chart labels **403 – Forbidden** | 403 label in demonstration screenshot is **not** R4 HTTP response proof |
| R5-E08 | https://portal.api.bot.or.th/terms | §4 considers BOT system/network outage; §5 prohibits interference; §6 protects credentials; §9 permits BOT to limit/change/discontinue services | Legal/operational policy only, not current health |
| R5-E09 | https://portal.api.bot.or.th/maintenance/BOT_API_Maintenance.html | Dated official temporary-maintenance announcement for 3 Oct 2026; Thai/English ending hours conflict | Dated notice, not a verified real-time status/uptime feed |
| R5-E10 | https://portal.api.bot.or.th/about-us | BOT API contact channel `botapi@bot.or.th` | Contact option only; no BOT confirmation request sent |
| R5-E11 | https://portal.api.bot.or.th/ | Official new platform/gateway/header identification | Does not establish current gateway operational health |

**Preservation level:** URL + observed date + claim, official static screenshots read but **not stored as immutable source artifacts**. No verified HTTP response/headers from gateway; no API-spec export history.

## 4. CURRENT DOCUMENTED PRODUCT/PLAN DISPLAYS

| BOT Product | Displayed Quota | Displayed Rate | Evidence | Status |
|---|---|---|---|---|
| Statistics | Unlimited | 2,000 calls / 1 hour | R5-E01 | `CONFIRMED_AS_CURRENT_DISPLAY` |
| Exchange Rates | Unlimited | 200 calls / 1 hour | R5-E02 | `CONFIRMED_AS_CURRENT_DISPLAY` |
| Interest Rates | Unlimited | 200 calls / 1 hour | R5-E03 | `CONFIRMED_AS_CURRENT_DISPLAY` |

**Important:** `Quota: unlimited` and an explicit `Rate` are **distinct UI configuration dimensions**; unlimited quota **does not justify unlimited instantaneous calls**. The BOT Product Plan is the authority for its **currently advertised display**, but not for implementation-level enforcement scope or window mechanics. Do not use one provider-wide rate constant.

**Unresolved manual-versus-product disagreement:** E05 static screenshot shows **1000/minute** for Statistics; E01 currently shows **2000/hour**. Both are official BOT surfaces. The static image is not dated/versioned for precise configuration provenance. `CONFIG_VINTAGE_OR_SCOPE_UNKNOWN`; **do not declare the screenshot obsolete as a fact** or apply it as live rate. This conflict was previously identified in R1/R2; R5 reconfirms it without claiming resolution.

## 5. ENFORCEMENT SCOPE — NOT PROVEN

| Question | R5 disposition | Evidence gap |
|---|---|---|
| Is the `2000/hour` cap per Account, Application, Token, Product, Subscription, API endpoint or combined key? | **UNKNOWN** | Official Product page displays rate only; no explicit enforcement key or test |
| Shared bucket across categorylist/observations/search-series? | **UNKNOWN** | Shared Product is documented, shared token bucket is not |
| Fixed vs sliding vs token-bucket window; start of hourly window and clock timezone? | **UNKNOWN** | No enforcement/window document or measured boundary |
| Concurrent calls and burst handling? | **UNKNOWN** | No BOT burst or concurrency contract found |
| Scope and semantics of unlimited quota vs rate limit? | **PARTIAL**: labels exist; precise accounting **UNKNOWN** | No official normative plan-definition text inspected |
| Plan/rate changes during subscription lifetime, old vs new token? | **UNKNOWN** | BOT Terms allow changes; propagation timing unspecified |
| Is there a BOT-wide default rate across all products? | **UNSUPPORTED / DO NOT ASSUME** | Different advertised product rates are directly observed |

The observation `Statistics Rate=2000/hour` must **never** automatically become `per-token 2000/hour` or `per-product cross-API 2000/hour` in a production configuration. Those are untested hypotheses.

## 6. RESPONSE HEADERS / RETRY SIGNALS

No live response was retrieved in R5. R3 had no credential; R4's attempted unauthenticated request failed at **local DNS** before HTTP. Therefore:

| Item | Verified current BOT Gateway behavior |
|---|---|
| HTTP status for over-limit requests (e.g. 429) | **UNKNOWN — NOT OBSERVED** |
| `Retry-After` header and its value format | **UNKNOWN — NOT OBSERVED** |
| `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset` | **UNKNOWN — NOT OBSERVED** |
| `X-RateLimit-*` variants | **UNKNOWN — NOT OBSERVED** |
| Rate-limit reset clock / throttling length | **UNKNOWN — NOT OBSERVED** |
| Response error envelope/content type/message | **UNKNOWN — NOT OBSERVED** |
| Safe automatic retry/backoff policy specific to BOT | **NOT PROVEN — NO ENGINE AUTHORIZED** |

Header names in this table are **inspection candidates**, not claimed BOT headers. Absence from the public pages inspected is **not proof of absence in real HTTP**. Do not infer conventional `401/403/429` meanings at the BOT contract level without evidence.

**Future observation contract (NOT code):** Capture actual HTTP status, response content type, non-secret allowlisted header names/values, `Retry-After` only if actually present, provider error envelope (redacted), UTC retrieval time, Product/Plan context, exact non-secret method/URL and request identity. Keep transport exceptions separate from origin HTTP responses. Never persist Token/Token Hash.

## 7. DEVELOPER PORTAL OPERATIONAL TELEMETRY

Manual §4 and the two official illustration images establish an **account-user Dashboard feature**, not an unauthenticated public operations API.

**Documented navigation:** Profile → Dashboard → Performance.

**Documented/illustrated features:**
- time-period overview (weekly example);
- total API calls, success/errors, aggregate error rate and average latency;
- selectable application on chart; success/error timeline;
- Export to CSV from charts;
- Top 5 highest error rates by API;
- Error breakdown.

**Crucial caution:** The R5-E07 screenshot contains an example error-breakdown label **`403 - Forbidden`**. This is *illustrative dashboard UI only*. It proves the interface can **display** a 403 category, **not** that Thailand Economic OS elicited an origin HTTP 403, not that every permission failure is 403, and not how BOT classifies authentication errors. R4 origin HTTP evidence remains zero.

**Dashboard UNKNOWNs:**
- exact CSV field names/schema, timezone, numeric semantics and data retention;
- whether charts contain all calls or aggregated/sampled records;
- update delay/accuracy and underlying data authority;
- visibility based on app owner, credential, subscription, or other roles;
- export privacy/security handling;
- existence of any sanctioned machine-readable telemetry endpoint.

Therefore the Dashboard is a **human operations cross-check candidate**, not a replacement for independently retained runtime HTTP evidence. Do not assert a real live API success/failure based on the Manual demo chart.

## 8. OFFICIAL MAINTENANCE: HISTORICAL NOTICE + NEW CROSS-LANGUAGE CONFLICT

The BOT-controlled notice at R5-E09 explicitly announces temporary unavailability for **3 October 2026**.

The **same official page** contains inconsistent end times:

| Text surface | Wording on BOT notice | Reading |
|---|---|---|
| Thai | `วันที่ 3 ตุลาคม 2569 เวลา 9:00 - 11:00 น.` | 09:00–11:00 (2-hour nominal window) |
| English | `on October 3, 2026, from 09:00 AM to 11:00 PM.` | 09:00–23:00 (14-hour nominal window) |

**R5-CONFLICT-02** — `OFFICIAL_BILINGUAL_TIME_CONTRADICTION / UNRESOLVED`.

R5 **cannot select** one ending time without a corrigendum or confirmation by BOT. The page is a **dated announcement**; it does not certify that maintenance occurred on schedule or that the gateway was down for either duration. It also **does not establish a current (8 October 2026) service outage**, a live status API, timezone convention, notice freshness/SLA, or post-maintenance restoration. Store both source strings in future operations evidence rather than silently preferring one language.

**Operational distinction:** `published maintenance notice` is a separate source role from `observed HTTP outage`, `portal user Dashboard telemetry`, `official real-time service status` (none verified), and `local DNS/egress fault` (R4). Do not equate them.

**Escalation candidate:** R5-E10 official BOT API support contact `botapi@bot.or.th` for bilingual time clarification and rate/headers questions. **No contact sent; no BOT reply claimed**.

## 9. OPERATIONAL SOURCE AUTHORITY MATRIX

| Question | Best authority available / required | What it cannot prove by itself |
|---|---|---|
| Product's advertised plan/rate today | Current BOT Product/Plan page | Token/app-specific enforcement |
| How to view aggregate calls/errors | BOT Manual + user-account Dashboard UI | Exact HTTP request log/schema/retention |
| What HTTP response the gateway gave | Actual safe retained gateway response | Cannot be substituted by manual demo / transport failure |
| How to time a planned maintenance window | Dated official notice + clarification where contradictory | Not a live current-health monitor |
| Whether BOT can revise service limits | BOT Terms §9 | Actual present limit/account config |
| Current outage/network health | Authorized live status signal or independent measured gateway access | No verified live status source in R5 |
| Retry/recovery signals | Verified current API spec and actual response headers | Generic HTTP conventions alone are not BOT proof |

## 10. R5 UNKNOWN REGISTER AND CLOSURE ROUTES

| ID | Open question | Evidence route |
|---|---|---|
| R5-U01 | Exact rate enforcement key (account/app/token/product/subscription/API)? | BOT explicit rate policy or bounded authorized observation; NOT a stress test |
| R5-U02 | Window algorithm/reset/burst/concurrency? | Official spec or safe measured response metadata, not a guessed bucket |
| R5-U03 | Does gateway actually emit `Retry-After`, `RateLimit-*`, `X-RateLimit-*`? | Capture allowlisted real response headers if naturally available; BOT explicit docs |
| R5-U04 | Actual throttle status/error response and recovery behavior? | BOT official contract or naturally encountered real throttle; do not force limit |
| R5-U05 | Dashboard CSV export schema, timezone, retention, lag, completeness? | Approved account dashboard sample with redaction; BOT policy/manual |
| R5-U06 | Current service-health/maintenance announcement discovery, publication/expiry policy and timezone? | Official BOT operational notice process/owner explanation |
| R5-U07 | 3 Oct 2026 Thai 11:00 vs English 23:00 official maintenance end time? | BOT corrected notice/direct clarification; preserve both now |
| R5-U08 | Manual screenshot 1000/min vs current product 2000/hour cause and applicable scopes? | Dated version or BOT config clarification / permitted app-plan evidence |
| R5-U09 | Provider error-state mapping under maintenance/network outage? | Official response contract + real HTTP; R4 blocker |
| R5-U10 | Product/Plan revision/history and impact on already approved apps? | BOT account/plan policy with version evidence |

Carry forward **BOT-U01..BOT-U09** and **D2-AUTH-U01..U11** unclosed. BOT-U06 (rate enforcement scope) remains UNKNOWN. BOT-U07 (spec export/history) remains UNKNOWN. No production-schema change is authorized by this R5 hypothesis set.

## 11. RESEARCH CONTRADICTIONS AND CLASSIFICATIONS

**R5-CONFLICT-01 — Rate screenshot versus current Product listing:** `CONFIG_SCOPE_OR_VINTAGE_UNKNOWN` (BOT Screenshot 1000/min vs current Statistics 2000/hour). Both are facts **at their own displayed-source level**; no current live enforcement conclusion.

**R5-CONFLICT-02 — 3 Oct maintenance Thai/English ending time:** `TRUE_TEXTUAL_CONTRADICTION / UNRESOLVED` (11:00 vs 23:00). Any maintenance duration derived from one language alone would be ungrounded.

**R5-NONCONFLICT-01 — Quota unlimited versus Rate finite:** `DIFFERENT_UI_DIMENSIONS`; not a contradiction. Exact enforcement semantics still UNKNOWN.

**R5-ILLUSTRATIVE-01 — Demo 403 label versus no measured R4 response:** `AUTHORITY_SCOPE_DIFFERENCE`; dashboard screenshot is not a real request trace and cannot close R4.

## 12. QUESTION → METHOD → EVIDENCE → FINDING → CONFIDENCE → UNKNOWN → IMPACT → NEXT QUESTION

- **QUESTION:** What is actually official today about limits, dashboard telemetry, retry headers and maintenance?
- **METHOD:** direct current BOT Product pages, Manual plus official screenshots, Terms and dated maintenance notice; targeted official-domain header queries; no gateway calls.
- **EVIDENCE:** R5-E01..E11; URL/date/claim based, no immutable source snapshot or raw authenticated response.
- **FINDING:** Statistics 2000/hour, Exchange Rates 200/hour, Interest Rates 200/hour are currently advertised with 'unlimited' quota; dashboard shows weekly/summary/error views and CSV export; dated maintenance notices exist; **same notice has bilingual schedule conflict**; enforcement scope/headers/retry mechanics are unproven.
- **CONFIDENCE:** HIGH for direct displayed plan values, Manual UI labels and official bilingual notice text; MEDIUM for freshness/applicability of unversioned screenshots; UNKNOWN for live HTTP behavior and current service health.
- **UNKNOWN:** R5-U01..R5-U10, BOT-U01..U09, D2-AUTH-U01..U11.
- **IMPACT:** Future connector must separate plan config (displayed), actual enforcement (unobserved), operational telemetry (Dashboard), scheduled notices and local transport fault. Nothing permits production retry/throttle assumptions.
- **NEXT QUESTION:** Day 02 **R6 — Secret & Security Model**: what is the least-exposure contract for approved credential provisioning, runtime injection, logging/CI masking, rotation/revocation and secret-free audit evidence, given the documented BOT Token / Token Hash ambiguity?

## 13. END-OF-ROUND STATUS / STOP BOUNDARY

- Day 01: FROZEN v1.1 / GATE PASS — unchanged.
- Day 02 R1/R2: recorded/documentary verification; no independent external semantic certification.
- Day 02 R3: live positive auth **BLOCKED** (`BOT-R3-CRED-01`).
- Day 02 R4: origin HTTP error behavior **BLOCKED** (`BOT-R4-EGRESS-01`).
- **Day 02 R5: DOCUMENTARY_RESEARCH_RECORDED_WITH_RUNTIME_UNKNOWNS** — not live Rate Limit PASS; no gateway calls/stress testing.
- Day 02 R6–R8: **NOT STARTED**. Next exact work R6 only.
- Day-02 Gate: **NOT ASSESSED**.
- Issue #11: **OPEN**. V0.2 production connector implementation: **HOLD**.
- Research Risk `BOT-R5-MAINT-01` added for unresolved bilingual maintenance timing; **not** claimed as a current production outage/blocker.
- **UNKNOWN ≠ PASS.**
