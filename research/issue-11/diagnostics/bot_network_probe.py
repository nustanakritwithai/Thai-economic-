#!/usr/bin/env python3
"""BOT network preflight: DNS, TCP/443, certificate+hostname TLS. No HTTP or tokens."""

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import socket
import ssl
import time

HOSTS = ("gateway.api.bot.or.th", "portal.api.bot.or.th")
TIMEOUT_SECONDS = 4.0


def probe_host(host, resolver=socket.getaddrinfo, socket_factory=socket.socket,
               context_factory=ssl.create_default_context, clock=time.monotonic):
    if host not in HOSTS:
        raise ValueError("Host not on exact BOT allowlist")
    record = {
        "host": host, "port": 443, "dns": "NOT_TESTED", "dns_answer_count": 0,
        "tcp": "NOT_TESTED", "tcp_attempts": 0, "tls": "NOT_TESTED",
        "tls_protocol": None, "failure_layer": None, "error_classes": [],
        "result": "NOT_TESTED", "http_requests": 0, "origin_http_status": None,
        "token_accessed": False, "authorization_sent": False,
    }
    try:
        info = resolver(host, 443, type=socket.SOCK_STREAM)
        addresses = [x for x in info if x[0] in (socket.AF_INET, socket.AF_INET6)]
    except (OSError, ValueError) as err:
        record.update(dns="BLOCKED", result="BLOCKED_DNS", failure_layer="DNS")
        record["error_classes"].append(type(err).__name__)
        return record
    record["dns_answer_count"] = len(addresses)
    if not addresses:
        record.update(dns="BLOCKED", result="BLOCKED_DNS", failure_layer="DNS")
        return record
    record["dns"] = "PASS"
    unique = []
    for addr in sorted(addresses, key=lambda x: 0 if x[0] == socket.AF_INET else 1):
        if not any((addr[0], addr[4]) == (other[0], other[4]) for other in unique):
            unique.append(addr)
        if len(unique) == 2:
            break
    for family, kind, proto, _, target in unique:
        raw = socket_factory(family, kind, proto)
        record["tcp_attempts"] += 1
        try:
            raw.settimeout(TIMEOUT_SECONDS)
            raw.connect(target)
            record["tcp"] = "PASS"
        except (OSError, ValueError) as err:
            record["error_classes"].append(type(err).__name__)
            raw.close()
            continue
        try:
            # Python default trust store, CA verification, SNI, hostname verification.
            ctx = context_factory()
            with ctx.wrap_socket(raw, server_hostname=host) as verified:
                record.update(tls="PASS_CA_AND_HOST_VERIFIED",
                              tls_protocol=verified.version(),
                              result="PASS_DNS_TCP_TLS", failure_layer=None,
                              error_classes=[])
                return record
        except (OSError, ValueError) as err:
            record["error_classes"].append(type(err).__name__)
        finally:
            raw.close()
    if record["tcp"] == "PASS":
        record.update(tls="BLOCKED", result="BLOCKED_TLS", failure_layer="TLS")
    else:
        record.update(tcp="BLOCKED", result="BLOCKED_TCP", failure_layer="TCP")
    return record


def make_evidence():
    results = [probe_host(host) for host in HOSTS]
    return {
        "schema_version": 1, "project": "Thailand Economic OS", "issue": 11,
        "research_day": 2, "scope": "GITHUB_RUNNER_DNS_TCP_TLS_ONLY",
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "runner": {"workflow_run_id": os.getenv("GITHUB_RUN_ID"),
                   "commit_sha": os.getenv("GITHUB_SHA"),
                   "runner_os": os.getenv("RUNNER_OS")},
        "hosts": results, "gateway_network_result": results[0]["result"],
        "http_requests_sent": 0, "bot_origin_http_status": None,
        "authentication_test": "NOT_PERFORMED", "credential_used": False,
        "r3_live_auth": "BLOCKED_NOT_TESTED_BY_THIS_DIAGNOSTIC",
        "r4_origin_http": "BLOCKED_NOT_TESTED_BY_THIS_DIAGNOSTIC",
        "day_02_gate": "BLOCKED_CRITICAL_EVIDENCE",
        "scope_note": "Transport from this runner only. No BOT HTTP/API/auth proof, "
                      "no inference about other runners or provider-wide outage.",
        "rule": "UNKNOWN != PASS",
    }


def make_summary(evidence):
    lines = [
        "# BOT no-token network preflight", "",
        "UTC: " + evidence["checked_at_utc"],
        "GitHub run: " + str(evidence["runner"]["workflow_run_id"]),
        "Commit: " + str(evidence["runner"]["commit_sha"]), "",
        "| Host | DNS | TCP:443 | TLS verification | Result |",
        "|---|---|---|---|---|",
    ]
    for h in evidence["hosts"]:
        lines.append("| {} | {} | {} | {} | {} |".format(
            h["host"], h["dns"], h["tcp"], h["tls"], h["result"]))
    lines += ["", "No HTTP, token, Authorization header, API request or stress test.",
              "PASS_DNS_TCP_TLS is only connectivity from this runner; not R3/R4 HTTP.",
              "Day-02 Gate remains BLOCKED_CRITICAL_EVIDENCE.", "", "UNKNOWN != PASS.", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="bot-network-evidence")
    args = parser.parse_args()
    evidence = make_evidence()
    dest = Path(args.output_dir)
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "network-evidence.json").write_text(
        json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (dest / "network-summary.md").write_text(make_summary(evidence), encoding="utf-8")
    # Emit only strictly nonsecret evidence for repository run provenance.
    print("BOT_NETWORK_EVIDENCE=" + json.dumps(evidence, sort_keys=True))
    return 0  # Connectivity blocked is a measured result, not a code/test failure.


if __name__ == "__main__":
    raise SystemExit(main())
