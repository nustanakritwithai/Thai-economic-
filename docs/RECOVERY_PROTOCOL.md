# Recovery Protocol

Use this whenever returning to the project after a break or when a new agent/team takes over.

## Canonical recovery sequence
1. Read `docs/PM_CONTROL.md`.
2. Confirm **ACTIVE VERSION**.
3. Read `releases/<active-version>.md`.
4. Inspect current `main` SHA and CI status.
5. Inspect open issues for the active release.
6. Read the latest release snapshot (if any).
7. Check blockers in `docs/RISKS.md`.
8. Read only the Decision Log entries relevant to the current task.
9. Ignore Parking Lot unless planning the next release.
10. Do not start NEXT until the current Release Gate passes.

## Source-of-truth rule
- Chat history is not authoritative project state.
- Human/AI memory is not authoritative project state.
- GitHub is authoritative for engineering/release state.
- Economic Database will be authoritative for numerical observations.
- Google Drive is authoritative for designated human-readable reports/plans where linked.

## Verification rule
Never infer completion from prose such as “done” or “looks good.”
Require commit/CI/test/evidence appropriate to the task.

## Handoff minimum
Every handoff must state:
- active version;
- main SHA;
- current issue/task;
- what changed;
- verification status;
- blockers/UNKNOWNs;
- exact next action.
