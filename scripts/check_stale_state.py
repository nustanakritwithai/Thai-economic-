#!/usr/bin/env python3
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "PROJECT_STATE.json"

def fail(msg):
    print(f"FAIL: {msg}")
    return False

ok = True

try:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
except Exception as exc:
    print(f"FAIL: cannot read PROJECT_STATE.json: {exc}")
    sys.exit(1)

required = [
    "project", "active_version", "active_release", "active_issue", "status",
    "current_gate", "next_exact_action", "blocked", "blockers",
    "last_verified_main", "last_verified_ci_run", "state_updated_at",
    "stale_after_days"
]
for key in required:
    if key not in state:
        ok = fail(f"PROJECT_STATE missing key: {key}") and ok

if state.get("project") != "Thailand Economic OS":
    ok = fail("PROJECT_STATE project name mismatch") and ok

active_version = state.get("active_version")
if not isinstance(active_version, str) or not re.fullmatch(r"V\d+\.\d+", active_version):
    ok = fail(f"invalid active_version: {active_version!r}") and ok

if not isinstance(state.get("active_issue"), int) or state.get("active_issue", 0) < 1:
    ok = fail("active_issue must be a positive GitHub issue number") and ok

if not str(state.get("next_exact_action", "")).strip():
    ok = fail("next_exact_action must not be empty") and ok

if state.get("blocked") and not state.get("blockers"):
    ok = fail("blocked=true requires at least one blocker") and ok

# Cross-check human-readable control files.
pm_text = (ROOT / "docs/PM_CONTROL.md").read_text(encoding="utf-8")
capsule_text = (ROOT / "docs/CONTEXT_CAPSULE.md").read_text(encoding="utf-8")

if active_version and f"**Active version:** {active_version} " not in pm_text:
    ok = fail("PROJECT_STATE active_version disagrees with PM_CONTROL") and ok

issue_token = f"#{state.get('active_issue')}"
if issue_token not in pm_text:
    ok = fail("PROJECT_STATE active_issue is not referenced by PM_CONTROL") and ok
if issue_token not in capsule_text:
    ok = fail("PROJECT_STATE active_issue is not referenced by CONTEXT_CAPSULE") and ok

release_path = ROOT / str(state.get("active_release", ""))
if not release_path.exists():
    ok = fail(f"active_release path does not exist: {state.get('active_release')}") and ok

# Stale-state detector:
# Fail only when repository work has continued significantly after the memory state
# was last refreshed. An idle repository does not become stale merely because time passes.
try:
    state_time = datetime.fromisoformat(state["state_updated_at"])
    commit_iso = subprocess.check_output(
        ["git", "show", "-s", "--format=%cI", "HEAD"],
        cwd=ROOT,
        text=True
    ).strip()
    commit_time = datetime.fromisoformat(commit_iso)
    stale_days = int(state["stale_after_days"])
    if commit_time > state_time + timedelta(days=stale_days):
        ok = fail(
            f"project memory is stale: latest commit {commit_iso} is more than "
            f"{stale_days} days after PROJECT_STATE update {state['state_updated_at']}"
        ) and ok
    else:
        print(
            f"PASS: stale-state window ({stale_days} days); "
            f"state={state['state_updated_at']} latest_commit={commit_iso}"
        )
except Exception as exc:
    ok = fail(f"stale-state timestamp check failed: {exc}") and ok

if not ok:
    sys.exit(1)

print(
    f"PASS: PROJECT_STATE coherent — {state['active_version']} / "
    f"issue #{state['active_issue']} / next action present"
)
