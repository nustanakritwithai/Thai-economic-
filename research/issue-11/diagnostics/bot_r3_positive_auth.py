#!/usr/bin/env python3
"""R3 research only: offline by default; no actual live work in public CI."""
import argparse
import http.client
import json
import os
from pathlib import Path
import socket
import ssl
from datetime import datetime, timezone
import time

HOST = "gateway.api.bot.or.th"
PATH = "/categorylist/category_list/"
TOKEN_ENV = "BOT_STATISTICS_API_TOKEN"
APPROVAL_FLAGS = ("BOT_R3_OWNER_APPROVED", "BOT_R3_STATISTICS_ACCESS_APPROVED",
                  "BOT_R3_PRIVATE_RUNNER_REVIEWED", "BOT_R3_SECRET_STORE_REVIEWED")
LIMIT = 262144


def receipt():
    return {
        "kind": "R3_POSITIVE_AUTH_RESEARCH_ONLY", "issue": 11, "day": 2,
        "target": "GET https://" + HOST + PATH,
        "source_sha256": "282a1ceb6e707e702957eb6d507f04a98dc4be48cc15ec9e1608c81a7c1f2fcd",
        "status": "NOT_EXECUTED", "request_count": 0, "http_status": None,
        "retrieved_at_utc": None, "content_type": None,
        "body_bytes_read": None, "category_count": None,
        "category_structure_valid": False, "redirects_followed": 0, "retries": 0,
        "secret_read": False, "secret_logged": False, "secret_source": "NOT_ACCESSED",
        "credentials_present_in_private_runner": "NOT_CHECKED",
        "exception_class": None, "elapsed_ms": None,
        "operational_security_certified": False, "positive_test_approved": False,
        "day02_gate": "BLOCKED_CRITICAL_EVIDENCE", "rule": "UNKNOWN != PASS",
    }


def preconditions(live=False, env=None):
    r = receipt()
    if not live:
        r["status"] = "BLOCKED_OFFLINE_PREFLIGHT_NO_REQUEST"
        return r, None
    if env is None:
        env = os.environ
    if not all(env.get(key) == "YES" for key in APPROVAL_FLAGS):
        r["status"] = "BLOCKED_APPROVAL_OR_PRIVATE_RUNNER_UNVERIFIED"
        return r, None
    token = env.get(TOKEN_ENV)
    if not isinstance(token, str) or not token:
        r["status"] = "BLOCKED_APPROVED_TOKEN_NOT_PROVISIONED_IN_THIS_RUNTIME"
        return r, None
    if len(token) > 8192 or "\r" in token or "\n" in token:
        r["status"] = "BLOCKED_UNSAFE_SECRET_VALUE"
        return r, None
    r["secret_read"] = True
    r["secret_source"] = "PROTECTED_PROCESS_ENV"
    r["credentials_present_in_private_runner"] = "PRESENT"
    return r, token


def probe(live=False, env=None, factory=http.client.HTTPSConnection,
          context_factory=ssl.create_default_context, clock=time.monotonic,
          utc_fn=lambda: datetime.now(timezone.utc).isoformat()):
    r, token = preconditions(live=live, env=env)
    if token is None:
        return r
    started = clock()
    c = None
    response = None
    try:
        # Exact BOT raw OpenAPI GET; no query, redirects, retries or token in URL.
        c = factory(HOST, 443, timeout=8, context=context_factory())
        r["request_count"] = 1
        c.request("GET", PATH, body=None, headers={
            "Authorization": token, "Accept": "application/json",
            "User-Agent": "Thai-Economic-OS-R3-Research/0.1", "Connection": "close"
        })
        response = c.getresponse()
        r["http_status"] = int(response.status)
        r["retrieved_at_utc"] = utc_fn()
        mime = str(response.getheader("Content-Type") or "").split(";", 1)[0].strip().lower()
        r["content_type"] = mime if mime in ("application/json", "text/html", "application/problem+json") else "UNVERIFIED_CONTENT_TYPE"
        if r["http_status"] != 200:
            r["status"] = "HTTP_OBSERVED_NO_POSITIVE_ACCESS_PROOF"
            return r
        if r["content_type"] != "application/json":
            r["status"] = "HTTP_200_UNEXPECTED_MIME_NOT_PASS"
            return r
        raw = response.read(LIMIT + 1)
        r["body_bytes_read"] = len(raw)
        if len(raw) > LIMIT:
            r["status"] = "HTTP_200_RESPONSE_TOO_LARGE_FOR_RESEARCH"
            return r
        try:
            data = json.loads(raw)
        except (ValueError, UnicodeDecodeError):
            r["status"] = "HTTP_200_UNPARSEABLE_JSON_NOT_PASS"
            return r
        categories = data.get("result", {}).get("category") if isinstance(data, dict) and isinstance(data.get("result"), dict) else None
        r["category_count"] = len(categories) if isinstance(categories, list) else None
        r["category_structure_valid"] = isinstance(categories, list) and len(categories) > 0 and all(isinstance(x, dict) for x in categories)
        r["status"] = ("HTTP_200_EXPECTED_CATEGORY_JSON_PENDING_HUMAN_REVIEW"
                       if r["category_structure_valid"] else
                       "HTTP_200_UNEXPECTED_RESPONSE_SHAPE_NOT_PASS")
        return r
    except Exception as exc:
        r["exception_class"] = type(exc).__name__
        r["status"] = "LOCAL_OR_TRANSPORT_FAILURE_NO_POSITIVE_PROOF"
        # No str(exc), stack locals, request/response headers, Token or raw body.
        return r
    finally:
        r["elapsed_ms"] = round((clock() - started) * 1000, 2)
        try:
            if response is not None:
                response.close()
            if c is not None:
                c.close()
        except Exception:
            pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("offline", "live"), default="offline")
    parser.add_argument("--out-dir", default="bot-r3-readiness")
    args = parser.parse_args()
    x = probe(live=args.mode == "live")
    x["run"] = {"id": os.getenv("GITHUB_RUN_ID"), "sha": os.getenv("GITHUB_SHA")}
    folder = Path(args.out_dir)
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "readiness.json").write_text(json.dumps(x, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (folder / "summary.md").write_text(
        "# BOT R3 research preflight\n\nResult: " + x["status"] +
        "\n\nGateway requests: " + str(x["request_count"]) +
        "\n\nHTTP status: " + str(x["http_status"]) +
        "\n\nDay-02 Gate: BLOCKED_CRITICAL_EVIDENCE\n\n"
        "No credentials, raw HTTP content or Authorization headers are retained.\n", encoding="utf-8"
    )
    print("BOT_R3_SAFE_READINESS=" + json.dumps(x, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
