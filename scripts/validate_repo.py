#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BASE_REQUIRED = [
    "docs/STRATEGIC_REVIEW_TEMPLATE.md",
    "releases/HANDOFF_TEMPLATE.md",
    "docs/BACKUP_RESTORE_POLICY.md",
    "docs/WEEKLY_CHECKPOINT_TEMPLATE.md",
    "PROJECT_STATE.json",
    "README.md",
    "index.html",
    "docs/NORTH_STAR.md",
    "docs/CONTEXT_CAPSULE.md",
    "docs/PM_CONTROL.md",
    "docs/MASTER_ROADMAP.md",
    "docs/ARCHITECTURE.md",
    "docs/DATA_CONTRACT.md",
    "docs/SOURCE_REGISTRY.md",
    "docs/AUDIT_STANDARD.md",
    "docs/AGENT_GOVERNANCE.md",
    "docs/DECISIONS.md",
    "docs/RISKS.md",
    "docs/PARKING_LOT.md",
    "docs/RECOVERY_PROTOCOL.md",
    "docs/DRIFT_REVIEW_TEMPLATE.md",
    ".github/ISSUE_TEMPLATE/active-release-task.md",
    "releases/V0.1.md",
    "releases/snapshots/V0.1-final.md",
    "schemas/source.schema.json",
    "schemas/series.schema.json",
    "schemas/observation.schema.json",
    "schemas/task.schema.json",
    "schemas/prediction.schema.json",
]

def fail(msg):
    print(f"FAIL: {msg}")
    return False

ok = True

for rel in BASE_REQUIRED:
    if not (ROOT / rel).exists():
        ok = fail(f"missing required file: {rel}") and ok

# PROJECT_STATE is the machine-readable NOW layer.
state = {}
state_path = ROOT / "PROJECT_STATE.json"
if state_path.exists():
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
        for key in ["active_version","active_release","active_issue","next_exact_action","state_updated_at"]:
            if key not in state:
                ok = fail(f"PROJECT_STATE missing key: {key}") and ok
        print("PASS: PROJECT_STATE machine-readable consistency fields")
    except Exception as exc:
        ok = fail(f"invalid PROJECT_STATE.json: {exc}") and ok

# Machine-readable schemas must at least parse as JSON.
for p in sorted((ROOT / "schemas").glob("*.json")):
    try:
        json.loads(p.read_text(encoding="utf-8"))
        print(f"PASS: JSON parse {p.relative_to(ROOT)}")
    except Exception as exc:
        ok = fail(f"invalid JSON {p}: {exc}") and ok

# Determine the active release from PM Control instead of hard-coding a version.
pm_path = ROOT / "docs/PM_CONTROL.md"
active_version = None
active_name = None
if pm_path.exists():
    pm_text = pm_path.read_text(encoding="utf-8")
    m = re.search(r"^- \*\*Active version:\*\* (V\d+\.\d+) (.+)$", pm_text, re.MULTILINE)
    if not m:
        ok = fail("PM_CONTROL must contain one canonical '**Active version:** Vx.y Name' line") and ok
    else:
        active_version, active_name = m.group(1), m.group(2).strip()
        print(f"PASS: active release parsed as {active_version} {active_name}")
    if "WIP limit:** 1 active version" not in pm_text:
        ok = fail("PM_CONTROL must enforce WIP limit = 1 active version") and ok
    if "UNKNOWN ≠ PASS" not in pm_text:
        ok = fail("PM_CONTROL must preserve UNKNOWN ≠ PASS") and ok
    for anchor in ["docs/NORTH_STAR.md", "docs/CONTEXT_CAPSULE.md"]:
        if anchor not in pm_text:
            ok = fail(f"PM_CONTROL must link strategic anchor {anchor}") and ok

# Active release contract must exist and carry strategic alignment.
if active_version:
    current_release = ROOT / f"releases/{active_version}.md"
    if not current_release.exists():
        ok = fail(f"missing active release contract: releases/{active_version}.md") and ok
    else:
        release_text = current_release.read_text(encoding="utf-8")
        if "**Status:** ACTIVE" not in release_text:
            ok = fail(f"{active_version} release contract must be ACTIVE while PM Control says it is active") and ok
        for phrase in ["WHY", "WHAT", "PROOF", "NEXT"]:
            if phrase not in release_text:
                ok = fail(f"{active_version} release contract missing strategic field: {phrase}") and ok
        if "UNKNOWN ≠ PASS" not in release_text:
            ok = fail(f"{active_version} contract must preserve UNKNOWN ≠ PASS") and ok
        print(f"PASS: active release contract releases/{active_version}.md")

# README cannot silently advertise a different active version.
readme_path = ROOT / "README.md"
if readme_path.exists() and active_version:
    readme_text = readme_path.read_text(encoding="utf-8")
    section = re.search(r"## Active version\s+\*\*(.+?)\*\*", readme_text, re.DOTALL)
    if not section:
        ok = fail("README must declare an Active version") and ok
    elif not section.group(1).startswith(active_version + " "):
        ok = fail(
            f"README active version '{section.group(1)}' disagrees with PM Control '{active_version} {active_name}'"
        ) and ok
    else:
        print("PASS: README active version matches PM Control")

# North Star and Context Capsule are required anti-drift anchors.
north = ROOT / "docs/NORTH_STAR.md"
if north.exists():
    t = north.read_text(encoding="utf-8")
    for phrase in [
        "Digital Economic Twin of Thailand",
        "Autonomous AI Economic Organization",
        "Autonomy must never exceed auditability",
        "One active version at a time",
    ]:
        if phrase not in t:
            ok = fail(f"NORTH_STAR missing invariant: {phrase}") and ok
    print("PASS: North Star invariants")

capsule = ROOT / "docs/CONTEXT_CAPSULE.md"
if capsule.exists():
    t = capsule.read_text(encoding="utf-8")
    for heading in [
        "## CURRENT",
        "## WHY CURRENT MATTERS",
        "## CURRENT GATE",
        "## NEXT EXACT ACTION",
        "## DO NOT DO YET",
    ]:
        if heading not in t:
            ok = fail(f"CONTEXT_CAPSULE missing recovery field: {heading}") and ok
    if active_version and active_version not in t:
        ok = fail("CONTEXT_CAPSULE does not mention active version") and ok
    print("PASS: Context Capsule recovery fields")

# Frozen Day-1 state must stay synchronized across machine and human recovery layers.
if state and state.get("day_01_gate") == "PASS":
    if not str(state.get("day_01_status", "")).startswith("FROZEN"):
        ok = fail("Day-1 gate PASS requires PROJECT_STATE day_01_status to be FROZEN*") and ok
    if state.get("next_planned_day") != 2:
        ok = fail("Day-1 gate PASS requires next_planned_day = 2") and ok
    if state.get("next_planned_round") not in (None, ""):
        ok = fail("Day-1 gate PASS must not keep a pending Day-1 next_planned_round") and ok

    for key in ["latest_research_artifact", "latest_machine_research_artifact"]:
        rel = state.get(key)
        if not rel:
            ok = fail(f"Day-1 gate PASS missing PROJECT_STATE {key}") and ok
        elif not (ROOT / rel).exists():
            ok = fail(f"PROJECT_STATE {key} points to missing file: {rel}") and ok

    required_r7_json = ROOT / "research/issue-11/day-01-r7-bot-contradictions.json"
    if not required_r7_json.exists():
        ok = fail("Day-1 gate PASS requires machine contradiction register day-01-r7-bot-contradictions.json") and ok

    pm_now = pm_path.read_text(encoding="utf-8") if pm_path.exists() else ""
    cap_now = capsule.read_text(encoding="utf-8") if capsule.exists() else ""
    for label, txt in [("PM_CONTROL", pm_now), ("CONTEXT_CAPSULE", cap_now)]:
        if "Day 1" not in txt or "FROZEN" not in txt:
            ok = fail(f"{label} must reflect Day 1 as FROZEN after Day-1 gate PASS") and ok
        if "Day 2 — BOT Authentication & API Behavior" not in txt:
            ok = fail(f"{label} must point to Day 2 after Day-1 gate PASS") and ok
        for stale in ["Current focus: **Day 1 Round 7", "Next planned round: **R8"]:
            if stale in txt:
                ok = fail(f"{label} contains stale post-freeze marker: {stale}") and ok
    print("PASS: Day-1 frozen-state synchronization")

# Issue template must prevent strategy-free work.
issue_template = ROOT / ".github/ISSUE_TEMPLATE/active-release-task.md"
if issue_template.exists():
    t = issue_template.read_text(encoding="utf-8")
    for heading in ["## WHY", "## WHAT", "## PROOF", "## NEXT"]:
        if heading not in t:
            ok = fail(f"active issue template missing {heading}") and ok
    print("PASS: WHY/WHAT/PROOF/NEXT issue contract")

# Basic series naming invariant.
pattern = re.compile(r"^[A-Z][A-Z0-9_]{2,95}$")
for sample in ["BOT_PCI_TOTAL", "TPSO_CPI_HEADLINE", "NESDC_GDP_REAL"]:
    if not pattern.match(sample):
        ok = fail(f"series ID convention failed sample {sample}") and ok
print("PASS: series ID convention samples")

if not ok:
    sys.exit(1)

print(f"PASS: project-control validation for active release {active_version}")
