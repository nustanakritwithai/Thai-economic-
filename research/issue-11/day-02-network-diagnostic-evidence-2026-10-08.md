# BOT Network Preflight — GitHub-hosted Runner Evidence (Day-02 Gap #1)

**Project:** Thailand Economic OS, V0.2 / Issue #11
**Date/time (UTC):** 2026-10-08T14:55:22.473994+00:00
**Source:** [GitHub Actions Run 37796439277](https://github.com/nustanakritwithai/Thai-economic-/actions/runs/37796439277) (job 113376986146, commit 961f16d662c50d61ad3ca764d2ec97bd0b1de009)
**Unit tests:** 6/6 PASS, checked in the same workflow run
**Evidence artifact:** bot-network-preflight-37796439277 (artifact ID 11558099575, stored in GitHub Actions)
**Classification:** PASS_GITHUB_RUNNER_DNS_TCP_TLS_ONLY
**Day-02 Gate:** BLOCKED_CRITICAL_EVIDENCE — NOT PASS
**Current work:** Day-02 Critical Evidence Gap Closure; Frozen v1 baseline preserved; no Day03.

## Question

The earlier Day-02 R4 agent runner failed DNS before HTTP. Is there an approved alternate GitHub-hosted runner where the current official BOT domain can resolve and accept TCP 443 and trusted TLS handshakes without credentials?

BOT official Migration Guide identifies gateway.api.bot.or.th: https://portal.api.bot.or.th/migration.

## Measured nonsecret observation

| Exact official BOT hostname | DNS | TCP 443 | TLS (CA + hostname) | Network layer |
|---|---|---|---|---|
| gateway.api.bot.or.th | PASS (4 addresses) | PASS (1 attempt) | PASS_CA_AND_HOST_VERIFIED — TLSv1.3 | PASS_DNS_TCP_TLS |
| portal.api.bot.or.th | PASS (4 addresses) | PASS (1 attempt) | PASS_CA_AND_HOST_VERIFIED — TLSv1.3 | PASS_DNS_TCP_TLS |

**Method:** One bounded GitHub Actions job (ubuntu-latest, Linux). Python socket DNS lookup, at most two TCP:443 attempts per hostname (actual attempts 1 each), Python SSL create_default_context with certificate authority and hostname verification. No HTTP request, no Authorization header, no API path or token.

The GitHub job printed BOT_NETWORK_EVIDENCE in its log. The record was parsed into the companion project JSON after exact commit/run identity and strict zero-HTTP/zero-credential invariants were checked. The workflow also retains its own JSON/Markdown ZIP artifact. **The GitHub Actions artifact bytes were not independently downloaded/checksummed here; the repository copy is derived from the GitHub job log.**

## Finding: local DNS limitation bounded, not erased

1. **CONFIRMED for this GitHub-hosted runner at 2026-10-08T14:55:22.473994+00:00:** DNS resolved four addresses for each host, TCP connected in one attempt for each, TLSv1.3 handshake succeeded with default CA and hostname checks. It is possible to use this environment for a future separately authorized BOT HTTP test.
2. **NOT CONFIRMED for prior R4 local runner or VPS/Android:** The earlier runner DNS failure (curl exit 6, http_code=000) remains historical evidence and its own environment remains unverified. Different egress/DNS providers can behave differently; the successful GitHub test does not prove the local runtime is repaired.
3. **NO BOT origin HTTP evidence:** HTTP request count 0, HTTP status null, response headers/content-type/body null; no provider-specific 401/403/429, success 200 or service uptime inference.
4. **R3 remains BLOCKED:** Approved BOT Statistics Token and account permissions were not accessed. This public diagnostic workflow must NEVER receive a real BOT secret.
5. **R4 remains BLOCKED for live error behavior:** Connectivity prerequisite is proven on a *different* runner but missing-Authorization HTTP request has not been executed. Its existing BOT-R4-EGRESS-01 risk is OPEN for the original context/origin error test.
6. **Day-02 Gate remains BLOCKED_CRITICAL_EVIDENCE**; no production connector or Day-03 authorization.

## Diagnostic safeguards / audit controls

- Allowlist is exactly gateway.api.bot.or.th and portal.api.bot.or.th; no redirects, no HTTP and no stress/load testing.
- GitHub workflow uses contents: read and does not inject GitHub/BOT secret values, run on untrusted PRs or build a connector.
- Six offline mocked unit tests cover DNS unavailable, empty resolution, TCP failure, TLS failure, exact allowlist, and successful TLS that must not become API PASS.
- Reported result scope is the *specific GitHub runner/time*, not a permanent BOT availability claim.
- CI structural validation for initial workflow addition: [run 37796439165](https://github.com/nustanakritwithai/Thai-economic-/actions/runs/37796439165), PASS.

## Exact next question

With GitHub-runner DNS/TCP/TLS now evidenced, can a separately approved **single harmless HTTP negative request** reach a verified **official BOT endpoint + method** without Authorization, and yield an actual sanitized provider HTTP status/headers? That would be an R4 additive follow-up, not proof of R3 approved authentication.

The separate R3 task requires a legitimate approved BOT Statistics Token delivered through a trusted private secret channel. Do **not** paste Token into ChatGPT or public GitHub.

No Frozen v1 or historical R1–R8 record has been retroactively changed.

**UNKNOWN ≠ PASS.**
