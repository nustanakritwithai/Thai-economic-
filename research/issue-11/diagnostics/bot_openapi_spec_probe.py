#!/usr/bin/env python3
"""Inspect one official public BOT Stat Category spec export; zero credentials or gateway calls."""
import argparse
from datetime import datetime, timezone
import hashlib
import http.client
import json
import os
from pathlib import Path
import re
import ssl
import time

HOST = "portal.api.bot.or.th"
PATH = "/portal/catalogue-products/statistics-1/d48f73217fdf41995a38859ed2b6e2d5/docs/download"
LIMIT_BYTES = 2_000_000
VERBS = ("get", "post", "put", "patch", "delete", "head", "options")
SAFE_PATH = re.compile(r"/[A-Za-z0-9/_{}.-]{1,160}$")
EXPECTED_BASE = "https://gateway.api.bot.or.th/categorylist"


def safe_mime(value):
    kind = str(value or "").split(";", 1)[0].strip().lower()
    return kind if re.fullmatch(r"[a-z0-9.+-]+/[a-z0-9.+-]+", kind) else None


def parse_spec(raw):
    try:
        content = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        return "NON_UTF8", None
    try:
        return "JSON", json.loads(content)
    except (ValueError, json.JSONDecodeError):
        try:
            import yaml
        except ImportError:
            return "YAML_PARSER_MISSING_OR_NOT_JSON", None
        try:
            return "YAML", yaml.safe_load(content)
        except yaml.YAMLError:
            return "INVALID_DOCUMENT", None


def summarize(obj):
    if not isinstance(obj, dict) or not isinstance(obj.get("paths"), dict):
        return None
    version = obj.get("openapi", obj.get("swagger"))
    if not isinstance(version, str) or not re.fullmatch(r"\d{1,2}\.\d{1,2}(?:\.\d{1,2})?", version):
        return None
    servers = []
    for item in obj.get("servers", []):
        if isinstance(item, dict) and isinstance(item.get("url"), str):
            u = item["url"]
            if re.fullmatch(r"https://gateway\.api\.bot\.or\.th/[A-Za-z0-9/_-]{1,100}", u):
                servers.append(u)
    if version.startswith("2.") and obj.get("host") == "gateway.api.bot.or.th":
        b = obj.get("basePath", "")
        if isinstance(b, str) and SAFE_PATH.fullmatch(b):
            servers.append("https://gateway.api.bot.or.th" + b)
    operations = []
    for path, content in sorted(obj["paths"].items()):
        if not isinstance(path, str) or not SAFE_PATH.fullmatch(path) or not isinstance(content, dict):
            continue
        methods = []
        for verb in VERBS:
            op = content.get(verb)
            if not isinstance(op, dict):
                continue
            responses = op.get("responses", {})
            codes = sorted(str(code) for code in responses if re.fullmatch(r"[1-5]\d\d|default", str(code))) if isinstance(responses, dict) else []
            methods.append({"method": verb.upper(), "documented_status_keys": codes})
        if methods:
            operations.append({"path": path, "methods": methods})
    schemes = obj.get("components", {}).get("securitySchemes", {}) if isinstance(obj.get("components"), dict) else {}
    if not isinstance(schemes, dict):
        schemes = {}
    if isinstance(obj.get("securityDefinitions"), dict):
        schemes = {**schemes, **obj["securityDefinitions"]}
    header_keys = [{"type": val.get("type"), "in": val.get("in"), "name": val.get("name")}
                   for val in schemes.values()
                   if isinstance(val, dict) and val.get("name") == "Authorization" and val.get("in") == "header"]
    cat = [o for o in operations if "category_list" in o["path"]]
    exact = next((m for o in cat if o["path"] == "/category_list/get"
                  for m in o["methods"] if m["method"] == "GET"), None)
    return {"spec_version": version, "server_urls": servers[:5],
            "paths_count": len(operations), "operation_count": sum(len(o["methods"]) for o in operations),
            "category_operations": cat,
            "exact_candidate_get_in_raw_spec": exact is not None,
            "exact_candidate_documented_status_keys": exact["documented_status_keys"] if exact else [],
            "expected_server_in_raw_spec": EXPECTED_BASE in servers,
            "security_schemes_authorization_header_only": header_keys}


def download(connection_factory=http.client.HTTPSConnection, ctx_factory=ssl.create_default_context):
    report = {
        "schema_version": 1, "issue": 11, "day": 2, "project": "Thailand Economic OS",
        "check": "PUBLIC_BOT_STAT_CATEGORY_RAW_OPENAPI_SPEC",
        "portal_host": HOST, "path": PATH, "request_method": "GET",
        "request_count": 0, "token_used": False,
        "http_status": None, "content_type": None, "bytes": None, "sha256": None,
        "document_format": None, "is_valid_openapi": False,
        "metadata": None, "candidate_get_method_proven": False,
        "raw_spec_retained_in_artifact": False,
        "classification": "NOT_EXECUTED", "transport_error_class": None,
        "elapsed_ms": None, "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "gateway_http_requests": 0, "bot_401_cause_verified": False,
        "day2_gate": "BLOCKED_CRITICAL_EVIDENCE", "rule": "UNKNOWN != PASS",
    }
    raw = None
    c = None
    begin = time.monotonic()
    try:
        c = connection_factory(HOST, 443, timeout=10, context=ctx_factory())
        report["request_count"] = 1
        c.request("GET", PATH, body=None, headers={
            "Accept": "application/json,application/yaml,text/yaml,application/octet-stream",
            "Connection": "close", "User-Agent": "Thai-Economic-OS-Public-OpenAPI-Research/0.1"
        })
        res = c.getresponse()
        report["http_status"] = int(res.status)
        report["content_type"] = safe_mime(res.getheader("Content-Type"))
        if res.status != 200:
            report["classification"] = "PUBLIC_SPEC_DOWNLOAD_NOT_200"
        else:
            raw = res.read(LIMIT_BYTES + 1)
            if len(raw) > LIMIT_BYTES:
                raw = None
                report["classification"] = "DOWNLOAD_EXCEEDS_SIZE_CAP"
            else:
                report["bytes"] = len(raw)
                report["sha256"] = hashlib.sha256(raw).hexdigest()
                fmt, data = parse_spec(raw)
                report["document_format"] = fmt
                meta = summarize(data)
                if meta is None:
                    report["classification"] = "DOWNLOADED_BUT_NOT_VERIFIED_OPENAPI"
                else:
                    report["is_valid_openapi"] = True
                    report["metadata"] = meta
                    report["candidate_get_method_proven"] = bool(
                        meta["exact_candidate_get_in_raw_spec"] and meta["expected_server_in_raw_spec"])
                    report["classification"] = (
                        "RAW_OFFICIAL_GET_OPERATION_AND_BASE_VERIFIED" if report["candidate_get_method_proven"]
                        else "RAW_OPENAPI_FOUND_BUT_CANDIDATE_PATH_OR_BASE_DIFFERENT")
    except (OSError, ValueError, http.client.HTTPException, ssl.SSLError) as ex:
        report["transport_error_class"] = type(ex).__name__
        report["classification"] = "PUBLIC_SPEC_DOWNLOAD_BLOCKED"
    finally:
        report["elapsed_ms"] = round((time.monotonic() - begin) * 1000, 2)
        if c is not None:
            c.close()
    return report, raw if report["is_valid_openapi"] else None


def summary(x):
    lines = ["# Public official BOT Stat Category OpenAPI retrieval", "",
             "Retrieval UTC: " + x["retrieved_at_utc"],
             "GET https://" + x["portal_host"] + x["path"],
             "Download HTTP status: " + str(x["http_status"]),
             "Raw bytes: " + str(x["bytes"]),
             "Raw SHA256: " + str(x["sha256"]),
             "Document format: " + str(x["document_format"]),
             "Classification: " + x["classification"],
             "Official GET method and path proven: " + str(x["candidate_get_method_proven"]),
             "Category operations:"]
    for row in (x["metadata"] or {}).get("category_operations", []):
        lines.append("- " + row["path"] + ": " + ", ".join(m["method"] for m in row["methods"]))
    return "\n".join(lines + ["", "No token or gateway HTTP call. R3 and Day-02 Gate remain BLOCKED.",
                              "This is official public spec evidence, NOT 401 error-cause proof.",
                              "UNKNOWN != PASS.", ""])


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output-dir", default="bot-official-openapi-evidence")
    args = p.parse_args()
    r, raw = download()
    r["run_provenance"] = {
        "run_id": os.getenv("GITHUB_RUN_ID"), "commit": os.getenv("GITHUB_SHA"),
        "runner_os": os.getenv("RUNNER_OS"),
    }
    folder = Path(args.output_dir)
    folder.mkdir(parents=True, exist_ok=True)
    if raw is not None:
        (folder / "official-stat-category-openapi.raw").write_bytes(raw)
        r["raw_spec_retained_in_artifact"] = True
    (folder / "spec-evidence.json").write_text(json.dumps(r, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (folder / "spec-summary.md").write_text(summary(r), encoding="utf-8")
    print("BOT_PUBLIC_OPENAPI_EVIDENCE=" + json.dumps(r, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
