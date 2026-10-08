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

# Frozen Day-2 research may be recoverable while its live API evidence Gate remains BLOCKED.
# This is repo consistency validation, NOT provider HTTP/security certification.
if state.get("day_02_research_freeze_status") == "FROZEN_v1_GATE_BLOCKED":
    import hashlib

    d2_prefix = "research/issue-11/"
    expected_freeze = d2_prefix + "day-02-bot-auth-FROZEN-v1.md"
    expected_machine = d2_prefix + "day-02-bot-auth-FROZEN-v1.json"
    expected_audit = d2_prefix + "day-02-closure-audit.md"
    expected_gate = d2_prefix + "day-02-gate.md"
    expected_refs = {
        "day_02_freeze_ref": expected_freeze,
        "day_02_freeze_json_ref": expected_machine,
        "day_02_closure_audit_ref": expected_audit,
        "day_02_gate_ref": expected_gate,
    }
    for key, expected in expected_refs.items():
        if state.get(key) != expected or not (ROOT / expected).is_file():
            ok = fail(f"Day-02 frozen blocked state requires {key} = {expected}") and ok

    required_state = {
        "day_02_gate": "BLOCKED_CRITICAL_EVIDENCE",
        "day_02_status": "RESEARCH_FROZEN_V1_GATE_BLOCKED",
        "day_02_round_08_status": "RECOVERY_FREEZE_COMPLETE_GATE_BLOCKED",
        "day_02_documented_auth": "PASS_DOCUMENTATION_ONLY_WITH_R2_CAVEATS",
    }
    for key, expected in required_state.items():
        if state.get(key) != expected:
            ok = fail(f"Day-02 frozen blocked PROJECT_STATE {key} must equal {expected}") and ok
    if state.get("day_02_next_round") not in (None, "") or state.get("current_research_day") != 2:
        ok = fail("Day-02 frozen blocked state must stay at Day 2 with no new R9") and ok
    if 2 in state.get("completed_research_days", []) or state.get("next_planned_day") != 2:
        ok = fail("Blocked Day-02 gate cannot be marked completed or promote planned day to Day 3") and ok
    if state.get("active_issue") != 11 or state.get("active_version") != "V0.2":
        ok = fail("Day-02 freeze must keep Issue #11 and V0.2 active") and ok
    if state.get("day_02_r8_recovery_self_audit") != "SAME_AGENT_RECOVERY_SELF_AUDIT_PASS_10_OF_10":
        ok = fail("Day-02 recovery self-audit must be explicit and not called external certification") and ok
    if state.get("day_02_r3_request_count") != 0 or state.get("day_02_r4_completed_gateway_http_exchanges") != 0:
        ok = fail("R3/R4 real HTTP evidence counts cannot be silently promoted") and ok
    if state.get("day_02_live_auth_test") != "BLOCKED_NO_USABLE_APPROVED_CREDENTIAL_IN_EXECUTION_CONTEXT":
        ok = fail("Day-02 blocked positive auth historical state must be retained") and ok

    # Integrity check of historical research artifacts using Git blob IDs.
    def git_blob_digest(path):
        raw = (ROOT / path).read_bytes()
        header = f"blob {len(raw)}\0".encode("ascii")
        return hashlib.sha1(header + raw).hexdigest()

    try:
        freeze = json.loads((ROOT / expected_machine).read_text(encoding="utf-8"))
        r7 = json.loads((ROOT / d2_prefix / "day-02-r7-bot-contradictions.json").read_text(encoding="utf-8"))
        r3 = json.loads((ROOT / d2_prefix / "day-02-r3-bot-positive-access-blocked.json").read_text(encoding="utf-8"))
        r4 = json.loads((ROOT / d2_prefix / "day-02-r4-bot-error-behavior-transport-blocked.json").read_text(encoding="utf-8"))
        r6 = json.loads((ROOT / d2_prefix / "day-02-r6-bot-secret-security.json").read_text(encoding="utf-8"))
        frozen_md = (ROOT / expected_freeze).read_text(encoding="utf-8")
        audit_md = (ROOT / expected_audit).read_text(encoding="utf-8")
        gate_md = (ROOT / expected_gate).read_text(encoding="utf-8")
    except Exception as exc:
        ok = fail(f"Day-02 frozen evidence JSON/Markdown unreadable: {exc}") and ok
    else:
        if freeze.get("profile_version") != "DAY02-FROZEN-v1" or freeze.get("day_02_gate") != "BLOCKED_CRITICAL_EVIDENCE":
            ok = fail("Day-02 freeze must be v1 with gate BLOCKED_CRITICAL_EVIDENCE") and ok
        if freeze.get("scope") != "DOCUMENTARY_RESEARCH_AND_RECOVERY" or freeze.get("day_03_authorized") is not False:
            ok = fail("Research freeze must not authorize Day 3 or imply runtime evidence") and ok
        if len(freeze.get("rounds", [])) != 8 or len(freeze.get("recovery_qa", [])) != 10:
            ok = fail("Day-02 freeze must preserve R1-R8 and ten recovery questions") and ok
        if freeze.get("r3_positive_auth", {}).get("request_count") != 0 or freeze.get("r3_positive_auth", {}).get("http_status") is not None or r3.get("live_auth_test", {}).get("request_count") != 0:
            ok = fail("R3 positive HTTP BLOCKED must preserve zero requests and null status") and ok
        if (freeze.get("r4_negative_error_behavior", {}).get("completed_gateway_http_exchanges") != 0 or
                freeze.get("r4_negative_error_behavior", {}).get("origin_http_statuses_observed") != [] or
                r4.get("completed_gateway_http_exchanges") != 0 or r4.get("origin_http_statuses_observed") != []):
            ok = fail("R4 negative HTTP BLOCKED must preserve zero origin responses") and ok
        if freeze.get("r6_security_model", {}).get("secret_manager_deployed") is not False or r6.get("actual_security_controls_verified") is not False:
            ok = fail("Security model remains design-only without runtime certification") and ok
        r7_sum = r7.get("summary", {})
        if r7_sum.get("case_count") != 19 or r7_sum.get("controlled_unknown_cases") != 8 or r7_sum.get("resolved_scope_or_authority") != 11:
            ok = fail("Day-02 R7 register must preserve 19 / 11 / 8 outcomes") and ok
        if freeze.get("r7_contradictions", {}).get("summary") != r7_sum:
            ok = fail("Frozen R7 contradiction summary disagrees with source register") and ok
        registry_lengths = (9, 11, 10, 12, 8)
        unknowns = freeze.get("unknown_registers", {})
        keys = ("bot_day01", "day02_auth", "day02_r5", "day02_r6", "day02_r7")
        if any(len(unknowns.get(k, [])) != n for k, n in zip(keys, registry_lengths)):
            ok = fail("Day-02 freeze must preserve all five open unknown registers 9/11/10/12/8") and ok
        if freeze.get("recovery_self_audit", {}).get("kind") != "SAME_AGENT_RECOVERY_SELF_AUDIT":
            ok = fail("Recovery audit independence must be labelled SAME_AGENT") and ok
        if freeze.get("recovery_self_audit", {}).get("independent_semantic_certification") is not False:
            ok = fail("Self-audit must NOT be represented as external independent certification") and ok
        if "Overall Day-02 evidence Gate: `BLOCKED_CRITICAL_EVIDENCE`" not in frozen_md:
            ok = fail("Frozen Markdown must explicitly present blocked Day-02 Gate") and ok
        if "**Overall result:** BLOCKED_CRITICAL_EVIDENCE" not in gate_md:
            ok = fail("Gate Markdown must explicitly remain BLOCKED") and ok
        if "SAME_AGENT_RECOVERY_SELF_AUDIT_PASS_10_OF_10" not in audit_md:
            ok = fail("Audit must preserve narrow self-audit scope") and ok
        if any(("**Q" + str(n) + ". ") not in frozen_md or ("**A" + str(n) + ".**") not in frozen_md for n in range(1, 11)):
            ok = fail("Frozen report missing one of ten recovery question/answer pairs") and ok
        for item in freeze.get("provenance_git_artifacts", []) + freeze.get("day01_frozen_provenance", []):
            path = item.get("path", "")
            expected_sha = item.get("git_blob_sha", "")
            if not path.startswith("research/issue-11/") or not (ROOT / path).is_file():
                ok = fail(f"Frozen provenance path missing/unsafe: {path}") and ok
            elif git_blob_digest(path) != expected_sha:
                ok = fail(f"Frozen historical Git blob drift: {path}") and ok
        for label, txt in [("CONTEXT_CAPSULE", cap_now), ("PM_CONTROL", pm_now)]:
            if "BLOCKED_CRITICAL_EVIDENCE" not in txt or "FROZEN" not in txt or "Day 2" not in txt:
                ok = fail(f"{label} must reflect Frozen Day-2 but BLOCKED Gate") and ok
            if "R8 NOT STARTED" in txt or "R8 (NOT STARTED)" in txt:
                ok = fail(f"{label} retains stale pre-freeze R8 marker") and ok
        print("PASS: Day-02 documentary research freeze and blocked-gate consistency")

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
