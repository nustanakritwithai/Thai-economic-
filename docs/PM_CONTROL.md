# Thailand Economic OS — PM Control

## Project state
- **Active version:** V0.2 Core Data Connectors
- **Status:** ACTIVE — PLANNING
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
- **Monthly drift review:** `docs/DRIFT_REVIEW_TEMPLATE.md`

## Primary goal
Implement a small, reliable set of official public-data connectors and prove retrieval, raw preservation, checksums, idempotency, and failure isolation before expanding data coverage.

## NOW
1. Inventory exact official P0 endpoints/files
2. Select minimum high-value series per source
3. Define connector interface and raw artifact convention
4. Implement BOT connector first
5. Add fixtures/tests
6. Repeat for NESDC, TPSO, MOF, Customs
7. Run V0.2 release gate

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
Read `docs/CONTEXT_CAPSULE.md` → `docs/NORTH_STAR.md` → this file → `releases/V0.2.md` → current issue → main/CI → continue only the current gate.

## Anti-drift rule
Every substantial task must answer **WHY → WHAT → PROOF → NEXT**. If the connection to the North Star is unclear, move it to Parking Lot and run a Drift Review before continuing.
