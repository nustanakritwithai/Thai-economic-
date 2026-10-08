#!/usr/bin/env python3
"""One-shot BOT read-only no-credential HTTP probe: research evidence, NOT authentication proof."""

import argparse
from datetime import datetime, timezone
import http.client
import json
from pathlib import Path
import re
import socket
import ssl
import time
import os

HOST = "gateway.api.bot.or.th"
PORT = 443
# BOT Stat Category documentation advertises base /categorylist and path /category_list/get.
# Official dynamically rendered API details did not expose a verifiable raw GET operation export.
# GET is deliberately chosen for one safe read-only negative candidate; not a proven schema method.
PATH = "/categorylist/category_list/get"
METHOD = "GET"
TIMEOUT_SECONDS = 7
REQUEST_HEADERS = {
    "Accept": "application/json",
    "User-Agent": "Thailand-Economic-OS-Research-NoAuth/0.1",
    "Connection": "close",
}
_ALLOWED_SAFE_MIME = re.compile(r"^([a-z0-9][a-z0-9.+_-]{0,32})/([a-z0-9][a-z0-9.+_-]{0,64})$", re.I)
_RATE_HEADER_NAMES = frozenset({
    "ratelimit-limit", "ratelimit-remaining", "ratelimit-reset",
    "x-ratelimit-limit", "x-ratelimit-remaining", "x-ratelimit-reset",
})
EXPECTED_RESPONSE_STATUS_RANGE = range(100, 600)


def classify_transport_error(error):
    if isinstance(error, socket.gaierror):
        return "DNS"
    if isinstance(error, (ssl.SSLError, ssl.CertificateError)):
        return "TLS"
    if isinstance(error, (socket.timeout, TimeoutError)):
        return "TIMEOUT"
    if isinstance(error, http.client.HTTPException):
        return "HTTP_RESPONSE_PARSING"
    if isinstance(error, OSError):
        return "TCP_OR_OTHER_TRANSPORT"
    return "LOCAL_CLIENT"


def sanitize_mime(header):
    if not header:
        return None
    candidate = str(header).split(";", 1)[0].strip()
    return candidate.lower() if _ALLOWED_SAFE_MIME.fullmatch(candidate) else "UNPARSEABLE_NOT_RETAINED"


def probe(*, connection_factory=http.client.HTTPSConnection,
          context_factory=ssl.create_default_context,
          monotonic=time.monotonic,
          utc_now=None):
    # Only one fixed host, path and GET method; no attacker input or redirect handling.
    # http.client does not automatically follow redirects and does not retry requests.
    record = {
        "schema_version": 1,
        "project": "Thailand Economic OS",
        "issue": 11,
        "research_day": 2,
        "gap": "R4_UNAUTHENTICATED_GATEWAY_HTTP_CANDIDATE",
        "target": {"host": HOST, "port": PORT, "path": PATH, "method": METHOD},
        "target_method_authority": "GET_CHOSEN_READ_ONLY; BOT_RAW_OPENAPI_METHOD_NOT_INDEPENDENTLY_CAPTURED",
        "target_path_authority": "OFFICIAL_BOT_STAT_CATEGORY_BASE_AND_INDEXED_OPERATION_PATH_COMPOSED",
        "request_count": 0,
        "authorization_header_present": False,
        "bot_token_read": False,
        "request_body_bytes": 0,
        "followed_redirect": False,
        "retry_count": 0,
        "response_body_read": False,
        "response_observed": False,
        "response_http_status": None,
        "sanitized_content_type": None,
        "content_length_header_integer": None,
        "response_header_presence": None,
        "elapsed_ms": None,
        "response_observed_at_utc": None,
        "failure_layer": None,
        "failure_exception_class": None,
        "classification": "NOT_STARTED",
        "bot_authentication_contract_pass": False,
        "bot_origin_error_semantics_verified": False,
        "day_02_gate": "BLOCKED_CRITICAL_EVIDENCE",
    }
    if not all(x not in REQUEST_HEADERS for x in ("Authorization", "X-API-Key", "Cookie")):
        raise RuntimeError("Credential-related headers must not be configured")

    started = monotonic()
    connection = None
    response = None
    try:
        context = context_factory()
        connection = connection_factory(
            HOST, port=PORT, timeout=TIMEOUT_SECONDS, context=context
        )
        record["request_count"] = 1
        connection.request(METHOD, PATH, body=None, headers=REQUEST_HEADERS)
        response = connection.getresponse()
        status = int(response.status)
        if status not in EXPECTED_RESPONSE_STATUS_RANGE:
            raise http.client.HTTPException("Unrecognized HTTP status")
        record["response_observed"] = True
        record["response_http_status"] = status
        record["response_observed_at_utc"] = (
            utc_now() if utc_now is not None else datetime.now(timezone.utc).isoformat()
        )
        record["sanitized_content_type"] = sanitize_mime(response.getheader("Content-Type"))
        raw_length = response.getheader("Content-Length")
        if raw_length and str(raw_length).isdigit():
            record["content_length_header_integer"] = int(raw_length)

        # Retain presence of named response headers only; NEVER any raw values/cookies.
        present = {name.lower() for name in response.headers.keys()}
        record["response_header_presence"] = {
            "www_authenticate": "www-authenticate" in present,
            "location": "location" in present,
            "retry_after": "retry-after" in present,
            "rate_limit": bool(present & _RATE_HEADER_NAMES),
            "server": "server" in present,
        }
        # A 200 might be an HTML login/error page; 401/403 can be edge/router or auth.
        # No body read, so never infer exact provider error cause from status alone.
        record["classification"] = "HTTP_RESPONSE_AT_BOT_GATEWAY_HOST_STATUS_UNINTERPRETED"
    except (OSError, ssl.SSLError, ssl.CertificateError, http.client.HTTPException, ValueError) as error:
        record["failure_layer"] = classify_transport_error(error)
        record["failure_exception_class"] = type(error).__name__
        record["classification"] = "NO_VALID_HTTP_RESPONSE_TRANSPORT_OR_PARSE_ERROR"
    finally:
        record["elapsed_ms"] = round((monotonic() - started) * 1000, 2)
        if response is not None:
            response.close()
        if connection is not None:
            connection.close()
    return record


def produce_evidence():
    result = probe()
    result["environment"] = {
        "provider": "GITHUB_ACTIONS",
        "workflow_run_id": os.getenv("GITHUB_RUN_ID"),
        "commit_sha": os.getenv("GITHUB_SHA"),
        "runner_os": os.getenv("RUNNER_OS"),
    }
    result["scope_limitations"] = [
        "HTTP response from verified gateway hostname may be generated by proxy/WAF or route layer",
        "Method GET is safe read-only test choice, not confirmed by captured official raw OpenAPI",
        "Absent Authorization does not prove exact BOT token-validation/error semantics",
        "No request/response body or raw headers were recorded",
        "One GET on one runner/time cannot prove service health, all routes or token access",
        "Prior R4 DNS failure on different runner remains historical evidence",
        "R3 remains BLOCKED without legitimately approved Token in private trusted runtime",
    ]
    result["rule"] = "UNKNOWN != PASS"
    return result


def summary(report):
    text = [
        "# BOT Stat Category — bounded GET without Authorization",
        "",
        "Runner UTC observation: " + str(report["response_observed_at_utc"]),
        "Run ID: " + str(report["environment"]["workflow_run_id"]),
        "Commit: " + str(report["environment"]["commit_sha"]),
        "Request: GET https://gateway.api.bot.or.th/categorylist/category_list/get",
        "Official raw OpenAPI GET method not captured; method selected as safe read-only candidate.",
        "Request attempts: " + str(report["request_count"]),
        "Response status (if observed): " + str(report["response_http_status"]),
        "Content type (sanitized): " + str(report["sanitized_content_type"]),
        "Measured elapsed ms (runner-side): " + str(report["elapsed_ms"]),
        "Classification: " + report["classification"],
        "Network/transport failure class: " + str(report["failure_layer"]),
        "Headers: allowlisted *presence only*; no raw values, bodies or secrets.",
        "R3 approved BOT Authentication: BLOCKED, not tested.",
        "R4 other errors and actual gateway auth semantics: UNKNOWN.",
        "Day-02 Evidence Gate: BLOCKED_CRITICAL_EVIDENCE.",
        "",
        "UNKNOWN != PASS.",
        "",
    ]
    return "\n".join(text)


def main():
    parser = argparse.ArgumentParser(description="Single no-token BOT GET probe")
    parser.add_argument("--output-dir", default="bot-http-negative-evidence")
    arguments = parser.parse_args()
    evidence = produce_evidence()
    folder = Path(arguments.output_dir)
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "http-evidence.json").write_text(
        json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (folder / "http-summary.md").write_text(summary(evidence), encoding="utf-8")
    print("BOT_HTTP_NEGATIVE_EVIDENCE=" + json.dumps(evidence, sort_keys=True))
    return 0  # HTTP response or transport error is evidence; not code test failure.


if __name__ == "__main__":
    raise SystemExit(main())
