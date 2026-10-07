# Risk & Blocker Register

## Active blockers
None at initialization.

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
