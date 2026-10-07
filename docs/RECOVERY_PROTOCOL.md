# Recovery Protocol

Use this whenever returning to the project after a break or when a new agent/team takes over.

## 60-second recovery sequence
1. Read `PROJECT_STATE.json` — machine-readable current truth.
2. Read `docs/CONTEXT_CAPSULE.md` — restore the current state.
3. Read `docs/NORTH_STAR.md` — restore the long-term WHY.
4. Read `docs/PM_CONTROL.md` — confirm WHERE/NOW.
5. Confirm **ACTIVE VERSION** and read `releases/<active-version>.md`.
6. Inspect current `main` SHA and CI status.
7. Inspect open issues for the active release.
8. Read the latest completed release snapshot.
9. Check blockers in `docs/RISKS.md`.
10. Read only Decision Log entries relevant to the current task.
11. Ignore Parking Lot unless planning future scope.
12. State one **NEXT EXACT ACTION** before doing work.
13. Do not start NEXT VERSION until the current Release Gate passes.

## WHY → WHERE → NOW → NEXT check
Before resuming, be able to answer:

- **WHY:** What is the North Star?
- **WHERE:** Which capability/version are we in?
- **NOW:** What exact gate/task is active?
- **NEXT:** What one action should happen next?

If any answer is unclear, do not create new scope. Run a North Star Drift Review first.

## Source-of-truth rule
- Chat history is not authoritative project state.
- Human/AI memory is not authoritative project state.
- `PROJECT_STATE.json` is the machine-readable NOW layer.
- `NORTH_STAR.md` is the long-term strategic anchor.
- GitHub is authoritative for engineering/release state.
- Economic Database will be authoritative for numerical observations.
- Google Drive is authoritative for designated human-readable reports/plans where linked.

## Verification rule
Never infer completion from prose such as “done” or “looks good.”
Require commit/CI/test/evidence appropriate to the task.

## Handoff minimum
Every handoff must state:
- North Star capability being advanced;
- active version;
- main SHA;
- current issue/task;
- WHY / WHAT / PROOF / NEXT;
- what changed;
- verification status;
- blockers/UNKNOWNs;
- exact next action.

## Long-break rule
If the project has been idle for more than one release cycle or the current state conflicts with the Roadmap:
1. freeze new work;
2. run `docs/DRIFT_REVIEW_TEMPLATE.md`;
3. reconcile PM Control, Context Capsule, release contract, issues, and Calendar;
4. resume only after one coherent current state is established.
