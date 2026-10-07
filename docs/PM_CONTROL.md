# Thailand Economic OS — PM Control

## Project state
- **Active version:** V0.1 Foundation
- **Status:** ACTIVE
- **WIP limit:** 1 active version
- **Engineering source of truth:** this GitHub repository
- **Human knowledge layer:** Google Drive Master Roadmap
- **Rule:** UNKNOWN ≠ PASS

## Primary goal
Freeze the minimum architecture, data contracts, governance, and verification rules required so V0.2 can add real public-data connectors without redesigning the foundation.

## NOW
1. Bootstrap repository topology
2. Freeze Architecture V0.1
3. Define Economic Data Contract
4. Define core JSON schemas
5. Register P0/P1 public data sources
6. Define audit IDs and traceability
7. Define Agent Governance baseline
8. Add CI validation
9. Verify GitHub Pages PM dashboard
10. Run V0.1 release gate

## CURRENT GATE — V0.1
- [ ] Repository topology complete
- [ ] PM Control complete
- [ ] GitHub Pages control dashboard verified
- [ ] Architecture baseline frozen
- [ ] Data Contract defined
- [ ] Core schemas validate
- [ ] Source Registry created
- [ ] Audit/ID convention defined
- [ ] Agent Governance baseline defined
- [ ] Recovery Protocol defined
- [ ] CI validation passes
- [ ] V0.1 verification evidence recorded

## BLOCKERS
None recorded at initialization. Any new blocker must be added to `docs/RISKS.md` and referenced from here.

## NEXT
**V0.2 Core Data Connectors**
- BOT
- NESDC
- TPSO CPI/PPI
- MOF
- Customs
- selected NSO data

V0.2 must not begin until every required V0.1 gate item is PASS.

## LATER
V0.3 Validation → V0.4 Economic Database → V0.5 Calculation → V0.6 Economic State → V0.8 Forecast → V1.0 Multi-Agent OS → V1.4 Policy Lab → V2.3 National Digital Twin → V3.0 Autonomous Economic Cabinet → V4.0 Thailand Economic OS.

New ideas go to `docs/PARKING_LOT.md`; they do not become active work automatically.

## Last verified
- Initial repository commit: `31f27d4d2c31e07f947031bc8ea79dcba3d49766`
- Active release contract: `releases/V0.1.md`

## Recovery shortcut
If returning after a break: read this file → read `releases/V0.1.md` → inspect main/CI/open issues → continue only the current gate.
