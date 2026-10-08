# Risk & Blocker Register

## Active blockers
- **BOT-R3-CRED-01 (OPEN, R3 positive live auth):** no usable approved BOT Statistics credential in this execution context. No conclusion about owner's account status or BOT outage.
- **BOT-R4-EGRESS-01 (OPEN, scoped R4 negative/error contract):** Original runner DNS failure remains history; raw BOT Stat Category OAS now verifies GET /category_list/, and no-token canonical GET observed HTTP401 (run 37826019253). Provider-specific error cause, remaining cases and original-runner remediation UNKNOWN; not R4 full PASS.
Both are scoped to missing live evidence, not global blockers of the Issue #11 research plan.

## BOT-R3-CRED-01 — Approved BOT Credential for Positive Authentication
**Status:** OPEN / BLOCKED ONLY FOR DAY-02 R3 LIVE POSITIVE AUTH.
**Owner:** authorized BOT Developer Portal account/Application administrator (approval/secret provision); research operator (single test/evidence after safe authorization).
**Affected:** V0.2, Issue #11, Day 02 R3 positive test and Day-02 Gate's live access evidence.
**Evidence:** BOT Manual https://portal.api.bot.or.th/manual specifies Approved Access before copied Token. In the 2026-10-08 R3 execution context, no legitimate usable approved Token and no authorized token-bearing runtime were available; zero HTTP requests were sent. Artifact: `research/issue-11/day-02-r3-bot-positive-access-blocked.md`.
**Impact:** documented auth PASS (docs-only); live positive auth BLOCKED, not HTTP failure and not PASS. No release gate closure.
**Workaround:** preserve blocked proof, continue R4 safe negative/error research without inferring real auth success or an HTTP error taxonomy. Do not paste tokens into chat or source control.
**Resolution:** app/Statistics entitlement approved; credential supplied to a trusted secret-injected runner; exact safe request operation verified; one actual successful response captured as sanitized telemetry in a separate additive artifact, with CI/review as appropriate.
**Non-goals:** no unauthorized account browsing, no secret inspection, no mock 200 and no production connector implementation.

**Day-2 Gap #5 environment check (2026-10-09):** Metadata-only GitHub Actions [run 37830244351](https://github.com/nustanakritwithai/Thai-economic-/actions/runs/37830244351) GET on bot-statistics-r3 Environment returned 404; complete public Environment list returned HTTP200 and did not contain that exact name. No reviewer/branch/bypass protections can be certified, and no Secrets were read. See research/issue-11/day-02-gap5-r3-environment-protection-evidence.md. This is **an owner/admin configuration dependency**, not proof of lacking BOT Account approval or Token elsewhere. R3 LIVE remains BLOCKED.
**Day-2 Gap #4 update (2026-10-09):** Research-only R3 offline harness was added, GitHub run 37828117237 passed 10/10 synthetic tests and a fail-closed OFFLINE receipt (0 real BOT HTTP and 0 actual credential access). Report research/issue-11/day-02-gap4-r3-offline-readiness.md. The first mock assertion failed on a common harmless field name; fixed with unique synthetic sentinel and test passed. No approved Application access, protected Environment/Secret store or privileged runner configured or verified. This does NOT close BOT-R3-CRED-01.

## BOT-R4-EGRESS-01 — Local DNS Prevents BOT Negative HTTP Observation
**Status:** OPEN / SCOPED TO DAY 02 R4 provider HTTP negative tests.
**Owner:** Research operator / authorized egress-runner/network administrator.
**Affected:** V0.2, Issue #11, Day 02 R4 negative/error behavior proof. Not a global project research blocker.
**Evidence:** R4-T01 attempted a read-only `GET` with absent Authorization to candidate `https://gateway.api.bot.or.th/categorylist/category_list/get` on 2026-10-08T10:30:29Z; curl exit code 6, resolver error; `http_code=000` is a curl no-response placeholder. R4-T00 also failed to resolve public BOT portal host. No origin HTTP response/status, content type, headers, size or server latency was observed. See `research/issue-11/day-02-r4-bot-error-behavior-transport-blocked.md`.
**Follow-up evidence (2026-10-09):** [GitHub Run 37822323186](https://github.com/nustanakritwithai/Thai-economic-/actions/runs/37822323186) sent exactly one no-Authorization GET to the candidate official base+path from a separate reachable GitHub-hosted runner, observed **HTTP 401 / application/json / Content-Length header 46** (no body read), elapsed 1357.92 ms. Official raw spec did not verify the GET Method; backend versus gateway/edge 401 cause is UNKNOWN. Evidence in `research/issue-11/day-02-r4-followup-http-2026-10-09.md` and `research/issue-11/day-02-r4-followup-http-2026-10-09.json`. The original curl exit 6 remains true for the original runner and historical R4 record. This is partial additional HTTP proof, not validated provider error taxonomy.
**Gap #3 addendum (2026-10-09):** Downloaded current official raw Stat Category OpenAPI v3.0.1/info v1.0.0 from public BOT Portal, original SHA256 `282a1ceb6e707e702957eb6d507f04a98dc4be48cc15ec9e1608c81a7c1f2fcd` archived at `research/issue-11/official-snapshots/BOT_Stat_Category_OpenAPI_v1.0.0_2026-10-09.json.gz`. It confirms **GET /category_list/** rather than prior `/category_list/get`, and GET /series_list/ requiring category; response schema declares 200 ONLY, not 401. A separate [canonical no-token GET run 37826019253](https://github.com/nustanakritwithai/Thai-economic-/actions/runs/37826019253) returned HTTP401 / application/json / Content-Length header 46, response body not read. This is one real status on the current exact OAS Method/Path, not proof of backend auth semantics, nor valid Token success. Preserve initial R4 and Gap2 wrong-path evidence unchanged. Supporting report `research/issue-11/day-02-gap3-canonical-http-2026-10-09.md`.
**Impact:** One actual 401 on the official canonical GET is observed, but 401 cause and behavior for malformed auth/403/429/method/parameters/permissions remain UNKNOWN. R3 positive Credential blocker remains independent.
**Workaround:** Retain local DNS evidence. A later GitHub-hosted no-auth network preflight **PASS** (run 37796439277, commit 961f16d662c50d61ad3ca764d2ec97bd0b1de009) independently confirmed DNS/TCP443/verified TLSv1.3 to both BOT official hosts, but not on the original runner and with **zero HTTP requests**. This provides an alternate tested network for later separately authorized safe origin HTTP probes, not R4 live HTTP PASS. See research/issue-11/day-02-network-diagnostic-evidence-2026-10-08.md.
**Resolution:** Original runner DNS must be resolved or its replacement explicitly approved. Correct canonical GET Method/Path is now known and one 401 observed, but full R4 closure still requires BOT-backed error-envelope/auth-cause interpretation and any relevant safe additional cases. One 401 and an OAS declaring only 200 do not establish full error taxonomy. Retain each historical attempt.
**Non-goals:** No secret harvesting, no credential sharing, no production connector implementation, no BOT outage claim.

## BOT-R5-MAINT-01 — Contradictory BOT Maintenance Notice Times
**Classification:** OPEN RESEARCH RISK / CONTRADICTION; **not** a current outage claim or a global blocker.
**Owner:** BOT API notice publisher for correction; Thailand Economic OS research operator for follow-up and evidence retention.
**Affected:** V0.2, Issue #11, Day 02 R5/R7 operational reliability and future maintenance-window interpretation.
**Evidence:** official BOT announcement https://portal.api.bot.or.th/maintenance/BOT_API_Maintenance.html for 3 October 2026 contains Thai `9:00 - 11:00 น.` versus English `09:00 AM to 11:00 PM`. They cannot both define the same exact end time. Both source strings are retained in `research/issue-11/day-02-r5-bot-rate-operations.md` and `.json`.
**Impact:** automated downtime calculation or maintenance scheduler could be wrong by 12 hours if silently choosing English or Thai wording. The page is a past dated notice, not real-time evidence of 8 October availability.
**Mitigation/workaround:** treat as ambiguous; preserve both literal strings and defer exact downtime-window interpretation. Current service health remains UNKNOWN. No automated maintenance handling from this research claim.
**Closure condition:** official corrected notice or explicit BOT API support confirmation resolving the scheduled end time and timezone; preserve earlier original evidence and document amendment. Official BOT API contact listed at https://portal.api.bot.or.th/about-us; **no contact sent**.

## BOT-R6-PUBLIC-LEAK-01 — Public Repository and Pages Secret Exposure Path
**Classification:** OPEN DESIGN RISK, not a confirmed leak or incident.
**Owner:** Future security lead and repository maintainer.
**Affected:** V0.2 Issue #11 R6 and future BOT connector security gate.
**Evidence:** public repo; inspected Pages workflow copies PROJECT_STATE.json, docs/, releases/, schemas/ into publicly deployed _site. Inspected validation workflow runs on push and PR with contents read. Neither file references BOT credentials; a full repo/configured Secrets scan was not performed. R6: research/issue-11/day-02-r6-bot-secret-security.md.
**Impact:** accidental Token or TOKEN HASH in tracked files, issues, workflow output or artifacts could be redistributed by Git history/Pages.
**Mitigation (NOT IMPLEMENTED):** trusted private secret facility/server worker, no BOT secret in general CI or Pages, synthetic canary leakage checks, independent security review and approval.
**Closure:** reviewed operational proof of secret-free repo/CI/Pages with canaries and restricted private runtime. Structural CI PASS alone is insufficient.

## R-001 — Source schema changes
**Risk:** Public agencies may change APIs/files without notice.
**Mitigation:** raw snapshots, parser tests, schema checks, source-health alerts.

## R-002 — Data revision leakage
**Risk:** Backtests accidentally use revised future knowledge.
**Mitigation:** mandatory vintages and release/retrieval timestamps.

## R-003 — Model overfitting
**Risk:** Complex models outperform in-sample but fail in production.
**Mitigation:** rolling out-of-sample benchmarks and challenger models.

## R-004 — Agent hallucination / correlated reasoning
**Risk:** Multiple agents repeat the same unsupported interpretation.
**Mitigation:** structured evidence, Red Team, authority boundaries, no majority-vote truth.

## R-005 — Automation loops / cost runaway
**Risk:** Agents create recursive tasks or excessive model usage.
**Mitigation:** task-depth limits, budgets, idempotency, escalation.

## R-006 — Scope drift
**Risk:** Digital Twin/policy ideas distract from current foundation.
**Mitigation:** WIP=1; Parking Lot; release gate.

## R-007 — Dashboard becomes source of truth
**Risk:** UI values diverge from database.
**Mitigation:** dashboard is read-only presentation of canonical APIs/database.

## Blocker policy
A blocker must include owner, affected version, evidence, workaround (if any), and resolution condition.
