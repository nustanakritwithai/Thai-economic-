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
