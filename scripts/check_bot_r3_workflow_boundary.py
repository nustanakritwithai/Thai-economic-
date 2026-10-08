#!/usr/bin/env python3
"""Enforce current public BOT research workflows stay secret-free and offline-only.
This is a static boundary check, NOT a full secret scan or a deployed secret store.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
OFFLINE_FILE = WORKFLOWS / "bot-r3-offline-readiness.yml"
ENV_FILE = WORKFLOWS / "bot-r3-env-metadata.yml"
SOURCE = ROOT / "research/issue-11/diagnostics/bot_r3_positive_auth.py"
STATE = ROOT / "PROJECT_STATE.json"
DENIED_WORKFLOW_SUBSTRINGS = (
    "secrets.", "BOT_STATISTICS_API_TOKEN", "--mode live", "--mode=live",
    "environment:", "pull_request_target", "pull_request:",
    "BOT_R3_OWNER_APPROVED", "BOT_R3_STATISTICS_ACCESS_APPROVED",
)
def verify():
    offline = OFFLINE_FILE.read_text(encoding="utf-8")
    metadata = ENV_FILE.read_text(encoding="utf-8")
    for path, body in [(OFFLINE_FILE, offline), (ENV_FILE, metadata)]:
        for pattern in DENIED_WORKFLOW_SUBSTRINGS:
            if pattern in body:
                raise AssertionError(f"Unexpected privileged R3 workflow pattern {pattern} in {path.name}")
        if "permissions:\n  contents: read" not in body:
            raise AssertionError(f"Research workflow must use read-only contents: {path.name}")
        if "workflow_dispatch:" not in body:
            raise AssertionError(f"Research workflow should remain auditable and manually runnable: {path.name}")
    if "--mode offline" not in offline or "bot_r3_positive_auth.py" not in offline:
        raise AssertionError("BOT R3 public readiness workflow no longer runs offline-only")
    if "--mode live" in metadata or "bot_r3_positive_auth.py" in metadata:
        raise AssertionError("Public metadata-only workflow must not invoke R3 credential-bearing code")
    py = SOURCE.read_text(encoding="utf-8")
    if 'choices=("offline", "live"), default="offline"' not in py:
        raise AssertionError("Default R3 script mode must remain offline")
    project = json.loads(STATE.read_text(encoding="utf-8"))
    if project.get("day_02_gate") != "BLOCKED_CRITICAL_EVIDENCE" or project.get("day_02_r3_request_count") != 0:
        raise AssertionError("Historical frozen R3 evidence must remain blocked and zero request")
    if project.get("day_02_gap5_status") != "R3_PUBLIC_ENVIRONMENT_TARGET_NOT_LISTED_OWNER_ACTION_REQUIRED":
        raise AssertionError("Missing observed public Environment protection diagnosis")
    if project.get("current_research_day") != 2 or project.get("completed_research_days") != [1]:
        raise AssertionError("A pending protected Environment cannot advance the research day")
    print("PASS: BOT R3 public workflows remain offline/metadata-only and secret-free")
    print("PASS: project R3/Day-02 evidence Gate remains BLOCKED")

if __name__ == "__main__":
    verify()
