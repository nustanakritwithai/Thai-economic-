#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "README.md",
    "index.html",
    "docs/PM_CONTROL.md",
    "docs/ARCHITECTURE.md",
    "docs/DATA_CONTRACT.md",
    "docs/SOURCE_REGISTRY.md",
    "docs/AUDIT_STANDARD.md",
    "docs/AGENT_GOVERNANCE.md",
    "docs/DECISIONS.md",
    "docs/RISKS.md",
    "docs/PARKING_LOT.md",
    "docs/RECOVERY_PROTOCOL.md",
    "releases/V0.1.md",
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
for rel in REQUIRED:
    if not (ROOT / rel).exists():
        ok = fail(f"missing required file: {rel}") and ok

for p in sorted((ROOT / "schemas").glob("*.json")):
    try:
        json.loads(p.read_text(encoding="utf-8"))
        print(f"PASS: JSON parse {p.relative_to(ROOT)}")
    except Exception as exc:
        ok = fail(f"invalid JSON {p}: {exc}") and ok

pm = (ROOT / "docs/PM_CONTROL.md")
if pm.exists():
    text = pm.read_text(encoding="utf-8")
    if "V0.1 Foundation" not in text or "WIP limit" not in text:
        ok = fail("PM_CONTROL must identify V0.1 and WIP limit") and ok
    else:
        print("PASS: PM Control active version/WIP rule")

release = ROOT / "releases/V0.1.md"
if release.exists():
    text = release.read_text(encoding="utf-8")
    if "UNKNOWN ≠ PASS" not in text:
        ok = fail("V0.1 contract must preserve UNKNOWN ≠ PASS") and ok
    else:
        print("PASS: V0.1 UNKNOWN rule")

pattern = re.compile(r"^[A-Z][A-Z0-9_]{2,95}$")
for sample in ["BOT_PCI_TOTAL","TPSO_CPI_HEADLINE","NESDC_GDP_REAL"]:
    if not pattern.match(sample):
        ok = fail(f"series ID convention failed sample {sample}") and ok
print("PASS: series ID convention samples")

if not ok:
    sys.exit(1)
print("PASS: repository V0.1 baseline validation")
