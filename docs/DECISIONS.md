# Decision Log

Decisions are append-only. Reversals create a new decision referencing the old one.

## DEC-001 — GitHub is Engineering Source of Truth
**Decision:** Code, schemas, release contracts, issues, PRs, CI evidence, and engineering state live in this repository.

## DEC-002 — Google Drive is Human Knowledge Layer
**Decision:** Long-form plans, executive reports, cabinet briefs, and human-readable working documents may live in Drive, but they do not replace engineering state in GitHub.

## DEC-003 — Vintage support is mandatory from the foundation
**Decision:** Economic observations must retain historical revisions so backtests use only information available at that time.

## DEC-004 — WIP limit = one active version
**Decision:** Only one release version may be ACTIVE. Future ideas go to Parking Lot.

## DEC-005 — UNKNOWN ≠ PASS
**Decision:** Missing verification evidence is not success.

## DEC-006 — LLMs do not own numerical truth
**Decision:** Connectors/validators/calculation engines/models create numerical artifacts under defined contracts; LLM agents interpret and coordinate.

## DEC-007 — Release by capability
**Decision:** A version closes only when its measurable capability gate passes, not because a calendar date arrived.

## DEC-008 — Auditability over autonomy
**Decision:** Automation may not become more autonomous than the system's ability to reproduce and inspect its actions.


## DEC-009 — North Star is a separate strategic authority
**Decision:** `docs/NORTH_STAR.md` defines the long-term WHY and changes rarely. Daily execution documents must not silently redefine the ultimate destination.

## DEC-010 — Project context must be recoverable without chat memory
**Decision:** `docs/CONTEXT_CAPSULE.md` must contain CURRENT / WHY CURRENT MATTERS / CURRENT GATE / NEXT EXACT ACTION / DO NOT DO YET so a new human or agent can resume from repository state.

## DEC-011 — Every active task uses WHY → WHAT → PROOF → NEXT
**Decision:** Work without a clear strategic WHY, bounded WHAT, verification PROOF, and explicit NEXT is not ready to start.

## DEC-012 — Monthly North Star Drift Review
**Decision:** At least monthly, review whether detailed execution remains aligned with the North Star, Roadmap, WIP=1 rule, active release scope, and architecture. Drift detection does not bypass Release Gates.


## DEC-013 — PROJECT_STATE.json is the machine-readable NOW authority
**Decision:** `PROJECT_STATE.json` is the canonical machine-readable summary of active version, active issue, current gate, blockers, verified baselines, and NEXT EXACT ACTION. Human-readable PM/Context files must agree with it.

## DEC-014 — Stale project memory is a CI failure
**Decision:** If repository work continues more than the configured stale window after PROJECT_STATE was refreshed, CI must fail until project memory is reconciled. Idle time alone does not make the state stale.

## DEC-015 — Weekly continuity checkpoints are operational hygiene
**Decision:** Run a short weekly checkpoint for continuity. It must not redesign strategy; uncertainty or contradiction escalates to a North Star Drift Review.

## DEC-016 — Backups are unproven until restore succeeds
**Decision:** For future Economic Database and raw evidence storage, backup existence is insufficient. Restore evidence becomes release-blocking starting with the database layer (V0.4).
