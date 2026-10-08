#!/usr/bin/env python3
"""Integrity check of official public BOT Stat Category snapshot and no-token HTTP observation."""
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = "research/issue-11/official-snapshots/BOT_Stat_Category_OpenAPI_v1.0.0_2026-10-09.json.gz"
MANIFEST = "research/issue-11/official-snapshots/BOT_Stat_Category_OpenAPI_v1.0.0_2026-10-09.manifest.json"
EVIDENCE = "research/issue-11/day-02-gap3-canonical-http-2026-10-09.json"
GZ_SHA256 = "663895274a24012b0bd816c32a6d72dea39fff37626f17c4036bc5ac67f82b48"
RAW_SHA256 = "282a1ceb6e707e702957eb6d507f04a98dc4be48cc15ec9e1608c81a7c1f2fcd"


def check(value, label):
    if not value:
        raise AssertionError(label)


def main():
    blob = (ROOT / ARCHIVE).read_bytes()
    check(len(blob) == 1483 and hashlib.sha256(blob).hexdigest() == GZ_SHA256,
          "archived gzip size/digest changed")
    raw = gzip.decompress(blob)
    check(len(raw) == 6799 and hashlib.sha256(raw).hexdigest() == RAW_SHA256,
          "raw official BOT OAS SHA256 changed")
    source = json.loads(raw)
    check(source["openapi"] == "3.0.1" and source["info"]["version"] == "1.0.0",
          "OpenAPI or API revision wrong")
    check(source["servers"][0]["url"] == "https://gateway.api.bot.or.th/categorylist",
          "official base URL changed")
    paths = source["paths"]
    check("get" in paths["/category_list/"], "category list GET operation missing")
    check("get" in paths["/series_list/"], "series list GET operation missing")
    p = paths["/series_list/"]["get"].get("parameters", [])
    check(any(x.get("name") == "category" and x.get("required") is True and
              x.get("schema", {}).get("type") == "string" for x in p),
          "required series list category parameter missing")
    check("401" not in paths["/category_list/"]["get"].get("responses", {}),
          "archived spec unexpectedly has defined 401 response")
    check(source["components"]["securitySchemes"]["clientIdHeader"] ==
          {"type":"apiKey","name":"Authorization","in":"header"},
          "Authorization security scheme mismatch")
    manifest = json.loads((ROOT / MANIFEST).read_text(encoding="utf-8"))
    check(manifest["original_sha256"] == RAW_SHA256 and
          manifest["gzip_sha256"] == GZ_SHA256 and manifest["gzip_path"] == ARCHIVE,
          "official source manifest mismatch")
    evidence = json.loads((ROOT / EVIDENCE).read_text(encoding="utf-8"))
    obs = evidence["observed"]
    check(evidence["spec_sha256"] == RAW_SHA256 and obs["raw_spec_sha256"] == RAW_SHA256,
          "observed GET not bound to official snapshot")
    check(obs["target"]["path"] == "/categorylist/category_list/" and
          obs["target"]["method"] == "GET", "observed canonical GET target wrong")
    check(obs["request_count"] == 1 and obs["response_observed"] and
          obs["response_http_status"] == 401, "single actual 401 observation changed")
    check(not obs["authorization_header_present"] and not obs["bot_token_read"] and
          not obs["response_body_read"], "unsafe credential or body handling")
    state = json.loads((ROOT / "PROJECT_STATE.json").read_text(encoding="utf-8"))
    check(state["day_02_gate"] == "BLOCKED_CRITICAL_EVIDENCE" and
          state["completed_research_days"] == [1],
          "Blocked Day-02 gate/complete-days invariant")
    check(state["day_02_r3_request_count"] == 0 and
          state["day_02_r4_completed_gateway_http_exchanges"] == 0,
          "Historic R3/R4 records must remain unchanged")
    print("PASS: BOT official raw OAS gzip SHA and source SHA")
    print("PASS: GET category_list/ and series_list/ operation/param")
    print("PASS: one no-Authorization 401 at official canonical GET")
    print("PASS: R3 and Day-02 gate remain BLOCKED, historical R4 zero preserved")


if __name__ == "__main__":
    main()
