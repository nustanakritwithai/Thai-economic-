# Thailand Economic OS — Context Capsule

> Read this first when returning after a break. It is intentionally short.

## PROJECT
Thailand Economic OS

## NORTH STAR
**Digital Economic Twin of Thailand + Autonomous AI Economic Organization**

Full anchor: `docs/NORTH_STAR.md`

## CURRENT
**V0.2 — Core Data Connectors**

Status: **ACTIVE — PLANNING / IMPLEMENTATION**

## WHY CURRENT MATTERS
V0.2 is not about “downloading government data.”

It establishes **reliable acquisition of numerical evidence** that every later layer depends on.

```text
V0.2 Reliable Acquisition
        ↓
V0.3 Reliable Validation/Normalization
        ↓
V0.4 Numerical Truth / Economic DB
        ↓
V0.6 Understand Present
        ↓
V0.8 Forecast Future
        ↓
V1.x Multi-Agent Economic Organization
        ↓
V2.x National Digital Twin
        ↓
V3–V4 Autonomous Economic Intelligence
```

If connector provenance, timestamps, checksums, idempotency, and failure behavior are weak now, every forecast and policy simulation later becomes less trustworthy.

## LAST COMPLETED
**V0.1 Foundation — COMPLETE**

Evidence:
- CI PASS
- GitHub Pages deployment PASS
- Snapshot: `releases/snapshots/V0.1-final.md`

## CURRENT RELEASE CONTRACT
`releases/V0.2.md`

## CURRENT ISSUE
**#11 — V0.2-01: Inventory official P0 data endpoints**

https://github.com/nustanakritwithai/Thai-economic-/issues/11

This is the single current execution entry point.

## CURRENT RESEARCH MODE
**Issue #11 Deep Research — 28-day planned window**

- Planned window: **2026-10-08 → 2026-11-04**
- Current planned day: **Day 1 COMPLETE / Week 1**
- Current focus: **Day 1 Round 2 COMPLETE — Independent Revalidation**
- Latest research artifact: `research/issue-11/day-01-r2-bot-ecosystem-revalidation.md`
- Day 1 rounds complete: **R1 Discovery, R2 Independent Revalidation**
- Next planned round: **R3 — Gap Hunt**
- Canonical plan: `docs/V0.2_ISSUE11_28_DAY_RESEARCH_PLAN.md`
- Calendar: **SYNCED** — Day 1–28 are scheduled as individual all-day project events in Asia/Bangkok, plus one 28-day research-window event.
- Extension is allowed. Calendar completion does not equal research PASS.

Research rule:
> Depth and evidence are the constraint; time is not the release gate.

Production connector implementation must not begin until Issue #11 is evidence-complete.

## CURRENT OBJECTIVE
Prove a small set of official P0 connectors end-to-end:
1. BOT
2. NESDC
3. TPSO
4. MOF
5. Customs

Do not ingest everything. Prove the pattern first.

## CURRENT GATE
A V0.2 connector is not complete until it proves:
- raw snapshot preservation;
- source identity;
- `retrieved_at`;
- checksum;
- parser version;
- rerun/idempotency behavior;
- isolated failure behavior;
- fixtures/tests;
- CI evidence.

## NEXT EXACT ACTION
Day 1 Round 3: hunt for what R1/R2 missed—especially the official downloadable List of Statistics APIs, possible BTWS table/report ↔ API series mappings, archive/version surfaces, and any missing metadata/discovery paths.

## DO NOT DO YET
- Full V0.3 normalization engine
- Production Economic Database
- GDP/CPI forecasting
- Economic State scoring
- Multi-Agent runtime
- Policy simulation
- Digital Twin

Future ideas go to `docs/PARKING_LOT.md`.

## RECOVERY PATH
```text
CONTEXT_CAPSULE
→ NORTH_STAR
→ PM_CONTROL
→ CURRENT RELEASE CONTRACT
→ current GitHub Issue
→ main SHA + CI
→ exact next action
```

## DRIFT CHECK
Before continuing, answer:
1. Does current work still support V0.2?
2. Does V0.2 still clearly support the North Star?
3. Has any future-version idea become active without passing the current gate?
4. Is the exact next action still explicit?

If any answer is unclear: stop new scope and run a North Star Drift Review.
