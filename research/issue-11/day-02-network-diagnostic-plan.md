# BOT Gateway network diagnostic — Issue #11 Day-02 gap

**Status:** DIAGNOSTIC HARNESS ADDED, run outcome not yet assessed.
**Day-02 Gate:** BLOCKED_CRITICAL_EVIDENCE unchanged.

Official BOT Migration Guide identifies gateway.api.bot.or.th (https://portal.api.bot.or.th/migration).
BOT Terms require non-disruption and protection of credentials (https://portal.api.bot.or.th/terms).

## Scope
One bounded GitHub Actions job tests only DNS, TCP/443, and TLS certificate plus hostname verification with standard Python SSL defaults for portal.api.bot.or.th and gateway.api.bot.or.th. Two IP attempts per host at most, four-second socket timeout. No HTTP/API operation, no Token, no Authorization and no stress/retries. This is a GitHub runner-only network result, NOT a BOT API success response, not a production connector, and does not demonstrate VPS/mobile connectivity.

## Artifacts
The workflow emits network-evidence.json, network-summary.md, and a sanitized BOT_NETWORK_EVIDENCE log line. Event triggers are a manual dispatch or changes to diagnostic files on main; no per-commit polling/recurring job is installed. Code logic uses offline unit tests.

## Gate boundaries
A PASS_DNS_TCP_TLS result means DNS/TCP/TLS succeeded for that host from that runner and date. It does NOT automatically close BOT-R4-EGRESS-01 because its original local DNS failure remains historical, and no origin HTTP response was obtained by this diagnostic. BOT-R3-CRED-01 remains open without approved Statistics access and trusted secret injection. Even both hosts passing transport must NOT turn the Day-02 evidence Gate to PASS.

UNKNOWN != PASS.
