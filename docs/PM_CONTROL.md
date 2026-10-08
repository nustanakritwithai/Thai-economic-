# Thailand Economic OS — PM Control

## Project state
- **Active version:** V0.2 Core Data Connectors
- **Status:** ACTIVE — DEEP RESEARCH
- **WIP limit:** 1 active version
- **Engineering source of truth:** this GitHub repository
- **Human knowledge layer:** Google Drive Master Roadmap
- **Rule:** UNKNOWN ≠ PASS

## Previous release
**V0.1 Foundation — COMPLETE**
- Verification baseline: `09594a1cec25876d97539340f188d6ac9c514bf7`
- CI PASS: run 37686940842
- Pages PASS: run 37686940970
- Snapshot: `releases/snapshots/V0.1-final.md`

## Strategic anchors
- **WHY:** `docs/NORTH_STAR.md`
- **WHERE:** `docs/MASTER_ROADMAP.md`
- **NOW / recovery:** `docs/CONTEXT_CAPSULE.md`
- **Current release:** `releases/V0.2.md`
- **Machine-readable NOW:** `PROJECT_STATE.json`
- **Weekly continuity:** `docs/WEEKLY_CHECKPOINT_TEMPLATE.md`
- **Monthly drift review:** `docs/DRIFT_REVIEW_TEMPLATE.md`
- **Semiannual strategy review:** `docs/STRATEGIC_REVIEW_TEMPLATE.md`
- **Backup/restore:** `docs/BACKUP_RESTORE_POLICY.md`

## Primary goal
Implement a small, reliable set of official public-data connectors and prove retrieval, raw preservation, checksums, idempotency, and failure isolation before expanding data coverage.

## Current research plan
- **Plan:** `docs/V0.2_ISSUE11_28_DAY_RESEARCH_PLAN.md`
- **Window:** 2026-10-08 → 2026-11-04
- **Current day:** Day 1 COMPLETE / Week 1
- **Current focus:** Day 1 frozen — BOT Data Ecosystem Map
- **Latest artifact:** `research/issue-11/day-01-bot-data-ecosystem-map.md`
- **Next planned day:** Day 2 — BOT Authentication & API Behavior
- **Rule:** planned calendar end does not authorize Issue #11 closure; critical UNKNOWNs extend the research period.
- **Implementation hold:** no production connector work until Issue #11 is evidence-complete.
- **Calendar sync:** 28 daily research events + 1 window event created in Google Calendar (Asia/Bangkok).

## Current execution issue
#11 — V0.2-01: Inventory official P0 data endpoints  
https://github.com/nustanakritwithai/Thai-economic-/issues/11

## NOW
1. Day 1 — BOT Data Ecosystem Map: **PASS for ecosystem mapping**
2. Next: Day 2 — BOT Authentication & API Behavior
3. Continue the 28-day Issue #11 research plan one day/question at a time
4. Preserve daily evidence logs and explicit UNKNOWNs
5. Complete Week 1 BOT → Week 2 NESDC/TPSO → Week 3 MOF/Customs → Week 4 validation/freeze
6. Do not define/implement the production connector until Issue #11 is complete
7. If Day 28 still has critical UNKNOWNs, extend Issue #11 instead of forcing PASS

## CURRENT GATE — V0.2
- [ ] BOT connector proof
- [ ] NESDC connector proof
- [ ] TPSO connector proof
- [ ] MOF connector proof
- [ ] Customs connector proof
- [ ] Idempotent rerun behavior
- [ ] retrieved_at/checksum/parser version on every retrieval
- [ ] Failure isolation between connectors
- [ ] Fixtures/tests
- [ ] CI PASS
- [ ] V0.2 verification snapshot

## BLOCKERS
None recorded at V0.2 opening. New blockers go to `docs/RISKS.md`.

## NEXT
**V0.3 Validation & Normalization**

Do not begin V0.3 until V0.2 gate is fully PASS.

## LATER
V0.4 Economic Database → V0.5 Calculation Engine → V0.6 Economic State → V0.8 Forecast → V1.0 Multi-Agent OS → V1.4 Policy Lab → V2.3 National Digital Twin → V3.0 Autonomous Economic Cabinet → V4.0 Thailand Economic OS.

New ideas go to `docs/PARKING_LOT.md`.

## Current references
- Active contract: `releases/V0.2.md`
- Master roadmap: `docs/MASTER_ROADMAP.md`
- Architecture: `docs/ARCHITECTURE.md`
- Data contract: `docs/DATA_CONTRACT.md`
- Source registry: `docs/SOURCE_REGISTRY.md`
- Recovery protocol: `docs/RECOVERY_PROTOCOL.md`

## Recovery shortcut
Read `PROJECT_STATE.json` → `docs/CONTEXT_CAPSULE.md` → `docs/NORTH_STAR.md` → this file → `releases/V0.2.md` → current issue → main/CI → continue only the current gate.

## Anti-drift rule
Every substantial task must answer **WHY → WHAT → PROOF → NEXT**. If the connection to the North Star is unclear, move it to Parking Lot and run a Drift Review before continuing.
