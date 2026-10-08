# Risk & Blocker Register

## Active blockers
- **BOT-R3-CRED-01 (OPEN, scoped to V0.2 Issue #11 / Day 02 R3 positive live auth):** no approved usable BOT Statistics token is available to the current authorized execution context. This is **not** proof of provider denial, account nonexistence, network failure or global project research blockage. Other evidence research (including R4 safe negative behavior) may continue. Details below.

## BOT-R3-CRED-01 — Approved BOT Credential for Positive Authentication
**Status:** OPEN / BLOCKED ONLY FOR DAY-02 R3 LIVE POSITIVE AUTH.
**Owner:** authorized BOT Developer Portal account/Application administrator (approval/secret provision); research operator (single test/evidence after safe authorization).
**Affected:** V0.2, Issue #11, Day 02 R3 positive test and Day-02 Gate's live access evidence.
**Evidence:** BOT Manual https://portal.api.bot.or.th/manual specifies Approved Access before copied Token. In the 2026-10-08 R3 execution context, no legitimate usable approved Token and no authorized token-bearing runtime were available; zero HTTP requests were sent. Artifact: `research/issue-11/day-02-r3-bot-positive-access-blocked.md`.
**Impact:** documented auth PASS (docs-only); live positive auth BLOCKED, not HTTP failure and not PASS. No release gate closure.
**Workaround:** preserve blocked proof, continue R4 safe negative/error research without inferring real auth success or an HTTP error taxonomy. Do not paste tokens into chat or source control.
**Resolution:** app/Statistics entitlement approved; credential supplied to a trusted secret-injected runner; exact safe request operation verified; one actual successful response captured as sanitized telemetry in a separate additive artifact, with CI/review as appropriate.
**Non-goals:** no unauthorized account browsing, no secret inspection, no mock 200 and no production connector implementation.

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
