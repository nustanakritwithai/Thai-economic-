# Thailand Economic OS — Day 02 R6
## BOT Secret & Security Model — Research Contract

**Date:** 2026-10-08, Asia/Bangkok
**Active release:** V0.2 Core Data Connectors
**Issue:** #11 (OPEN)
**Result:** SECURITY_DESIGN_RECORDED_NOT_IMPLEMENTED
**Day-02 Gate:** NOT ASSESSED
**R3 live positive authentication:** BLOCKED, BOT-R3-CRED-01
**R4 live origin HTTP errors:** BLOCKED, BOT-R4-EGRESS-01
**R5:** Documentary evidence recorded, enforcement/Retry-After UNKNOWN
**R7 / R8:** NOT STARTED
**Production connector:** HOLD
**Day-01 Frozen v1.1:** PRESERVED

## 1. QUESTION

How must future Thailand Economic OS protect BOT Statistics credentials against leaks through the public GitHub repository, Pages, CI, logs, URL, screenshots, AI agents, and token rotation/revocation? Which rules come directly from BOT or GitHub and which are only project design recommendations?

## 2. EVIDENCE & METHOD

Inspected Day-02 R1–R5 research and live current official BOT Manual/Terms/Migration. Studied first-party GitHub Actions Secrets/Secure-Use/Environments documentation and OWASP recommendations. Read current PUBLIC repository metadata and its two workflows at main ee7ff6dd4852989751d221362b68394b04d7816a. No BOT Portal login, credential read, Secrets settings access, live Gateway request, secret rotation, runtime deployment, connector implementation or CI workflow modification was performed.

| ID | Source and authority scope | URL |
|---|---|---|
| R6-E01 | BOT Manual; approved access then Token copy and Authorization header | https://portal.api.bot.or.th/manual |
| R6-E02 | BOT Terms §6 access secrecy, §5 safety, §9 change rights | https://portal.api.bot.or.th/terms |
| R6-E03 | BOT new Gateway and Authorization vs legacy migration | https://portal.api.bot.or.th/migration |
| R6-E04 | BOT illustrative APP ID/TOKEN/TOKEN HASH, ROTATE/REVOKE UI | https://portal.api.bot.or.th/assets/images/manual/Illustration%209.png |
| R6-E05 | GitHub encrypted Actions Secrets scopes | https://docs.github.com/en/actions/concepts/security/secrets |
| R6-E06 | GitHub secret masking limits, least privilege, untrusted workflows | https://docs.github.com/en/actions/reference/security/secure-use |
| R6-E07 | GitHub secrets in workflows, fork PR restrictions | https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets |
| R6-E08 | GitHub Environments and reviewer approvals | https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments |
| R6-E09 | OWASP general secret management, audits, revoke/rotation | https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html |
| R6-E10 | Actual read-only project validation CI workflow | https://github.com/nustanakritwithai/Thai-economic-/blob/ee7ff6dd4852989751d221362b68394b04d7816a/.github/workflows/validate.yml |
| R6-E11 | Actual public GitHub Pages workflow | https://github.com/nustanakritwithai/Thai-economic-/blob/ee7ff6dd4852989751d221362b68394b04d7816a/.github/workflows/pages.yml |
| R6-E12 | Repository visibility: PUBLIC | https://github.com/nustanakritwithai/Thai-economic- |

Evidence consists of checked URLs, BOT/GitHub source roles and date, and exact repo blob/commit anchors. No immutable external official webpage snapshot or source checksum is claimed. R6 did not inspect GitHub configured Secrets values, Environment protections or any private access rights.

## 3. BOT FACTS VS UNPROVEN CREDENTIAL SEMANTICS

DOCUMENTED by BOT: Developer Account -> Product/Plan -> Application request -> Approved Access -> hidden Token becomes visible -> copy Token -> HTTP Authorization header -> current gateway.api.bot.or.th. Account/cart submission is not permission approval. BOT Terms require access means to be protected from disclosure; Migration Guide replaces X-IBM-Client-Id and legacy gateway.

ILLUSTRATIVE UI only: APP ID, TOKEN and TOKEN HASH are separate fields; authToken, ROTATE, REVOKE and EXPIRES: Never appear in BOT Manual screenshot. The exact on-wire role of TOKEN HASH, credential expiry, refresh, rotation overlap, immediate revocation effects, app/product scope and whether Bearer is required/rejected are UNKNOWN. Never treat TOKEN HASH as a safe public digest, a replacement for TOKEN, or an automatically accepted header.

PROJECT DESIGN classification:
- BOT TOKEN = SECRET, never repo/chat/logs/browser.
- BOT TOKEN HASH = SECRET / provider-specific usage UNKNOWN.
- APP ID = confidential-by-default identifier pending provider/owner clarification.
- BOT Portal Account and Approved Access = sensitive/private authorization metadata; no real account IDs in public artifacts.
- GITHUB_TOKEN = GitHub-only workflow identity, NOT BOT API credential.
- GitHub OIDC may authenticate approved cloud secret managers, but BOT direct OIDC capability is UNKNOWN. No BOT federation claim.

## 4. REAL CURRENT REPOSITORY TRUST BOUNDARY

Repository is PUBLIC. Current validate.yml runs on push/main and pull_request/main with contents: read, executes project-control scripts and does NOT explicitly reference a BOT Token. This CI is structural validation, not a full secret-scan/redaction certification.

Current pages.yml is a public static deployment: copies index.html, PROJECT_STATE.json, docs/, releases/ and schemas/ to _site. Its id-token: write and pages: write are GitHub Pages deployment permissions, not BOT authentication permissions. Neither inspected workflow references BOT credential values; that does NOT prove GitHub settings contain no Secrets or that full repo is leak-free.

Risk BOT-R6-PUBLIC-LEAK-01: accidentally committing BOT credentials into tracked JSON/MD/CI logs can expose them via public Git history, Issues/PR, CI artifact or Pages output. This is a future EXPOSURE PATH, not an observed secret leak or current incident.

## 5. PROPOSED TRUST FLOW — NOT IMPLEMENTED

    HUMAN BOT ACCOUNT ADMIN + APPROVED STATISTICS PRODUCT
                      |
                      v
    PRIVATE MANAGED SECRET STORE (NOT SELECTED/DEPLOYED)
                      |
                      v
    DEDICATED TRUSTED SERVER-SIDE API WORKER (NOT BUILT)
                      |
                      v
    VERIFIED HTTPS BOT GATEWAY WITH AUTHORIZATION HEADER
                      |
                      v
    SAFE RESPONSE CLASSIFICATION / SECRET-FREE AUDIT RECEIPT
                      |
                      v
    NONSECRET PROJECT DATA / PUBLIC GITHUB / PAGES / AGENTS

Only the legitimate BOT account/application administrator provisions credentials through a trusted path into a restricted PRIVATE secret facility. Do not ask user to paste raw Token or TOKEN HASH in ChatGPT, GitHub comments or research. Maintain opaque nonsecret secret_ref, app/product intent, approval status, owner and audit time in a protected governance record.

Future worker retrieves secret at run time by narrow scoped identity. If an environment variable is used, inject per job/process, never project-global; environment variables themselves can leak in debug/process inspection and are not a full security boundary. Never put credentials in shell argv, URLs/query, environment dump, screenshots, client-side JavaScript or static Pages. Construct Authorization only inside a trusted HTTPS worker; validate exact official gateway host and TLS certificate; do not forward Authorization on cross-origin redirects. No fallback to legacy X-IBM-Client-Id, token in URL, or fabricated success.

## 6. PROPOSED CI AND AI AUTHORITY RULES — NOT IMPLEMENTED

Existing PR/validate and Pages jobs must remain BOT-secret-free. A future legitimate positive BOT test, if needed, must have a separate trusted job/runner and explicit human/Environment approval, least-privilege scopes, trusted code/branch, independently reviewed actions, no untrusted pull_request_target checkout, and preferably full commit-SHA pinned actions before privileged access. This is recommended control design only; no workflow/secret configuration changed during R6.

GitHub automatic secret redaction is NOT guaranteed: transformations, Base64, URL encoding, partial strings, stderr, debug headers or third-party Actions can leak. Masking is last-resort defense, not a license to print. Never log Authorization, TOKEN, TOKEN HASH, Cookie/Set-Cookie, Proxy-Authorization, full request headers, raw error stack locals, provider dashboard exports or secret fingerprints/prefixes/suffixes.

AI Agents may use sanitized economic observations and reports; they must not see/tokenize/store/rotate credentials merely because they have tool access. Any privileged change to credential or Actions Secret requires separate authorization and audit.

## 7. PROPOSED RECEIPT AND TEST GATES

Allowed nonsecret receipt fields only when actually observed: provider, product, API name, opaque nonsecret credential reference, safe request identifier and path, actual method/status, UTC retrieved_at only after HTTP response, content type, byte count, latency, allowlisted non-sensitive response header fields, transport error classification, source checksum/vintage for public permitted economic data.

If DNS/TCP/TLS fails before HTTP, provider HTTP status, response headers, response bytes and provider response timestamp remain NULL. Curl http_code=000 is a local no-response sentinel, NOT a BOT HTTP code. Prior R3 and R4 evidence stays unchanged.

Synthetic canary tests (never live BOT Token) will eventually verify that source code, config, stdout/stderr, exceptions, GitHub Actions artifacts, Git history and Pages _site do not leak secrets. An actual real BOT response still requires the R3 authorized test and must never be simulated.

| Gate | Necessary future evidence | R6 status |
|---|---|---|
| SEC-G01 | Approved BOT Statistics entitlement without exposing token | R3 BLOCKED |
| SEC-G02 | Chosen private secrets facility and restricted worker identity | NOT IMPLEMENTED |
| SEC-G03 | Separate PR/validate/Pages public build from any secret job | EXISTING WORKFLOW FILES INSPECTED ONLY |
| SEC-G04 | Synthetic canary leakage checks for logs/CI/artifacts/Pages | NOT TESTED |
| SEC-G05 | TLS, destination host and no Authorization-on-redirect tests | NOT IMPLEMENTED |
| SEC-G06 | Server-side only BOT Token insertion | NOT IMPLEMENTED |
| SEC-G07 | Transport vs provider HTTP null-safe logging | R4 BLOCKED, NOT IMPLEMENTED |
| SEC-G08 | Actual safe positive BOT HTTP response | R3 BLOCKED |
| SEC-G09 | BOT-backed rotate/revoke procedure/expiry | UNKNOWN |
| SEC-G10 | Public repo, Pages and Git history secret scanning | NOT IMPLEMENTED |
| SEC-G11 | Human approval, pinned dependencies and job permissions | NOT IMPLEMENTED |
| SEC-G12 | Credential lifecycle audit and incident evidence retention | NOT IMPLEMENTED |

No SEC-G control is operationally certified PASS during R6. A design requirement is not an implemented control.

## 8. PROPOSED ROTATION/REVOCATION/INCIDENT RUNBOOK

1. Authorised admin validates current BOT entitlement and actual lifecycle behavior. Do not infer global expiry Never from screenshot.
2. On scheduled review, prepare replacement privately if permitted, then test only through a trusted runner using approved R3 procedure.
3. Switch the worker's secret reference, then revoke old credential according to confirmed BOT overlap behavior. If compromise occurs, prioritize immediate containment/revoke, even if availability drops.
4. Stop affected jobs, review access and log exposure, invalidate old credentials, remove private copies, sanitize published artifacts as needed. Deleting Git commit alone never restores safety after a leak.
5. Verify revocation only through safe authorised evidence; never assume 401/403 without BOT response.
6. Retain nonsecret who/what/when/approval/incident receipts, not token values or hashes.

No Token was acquired, rotated or revoked; no actual leakage incident is asserted.

## 9. R6 OPEN UNKNOWN REGISTER

| ID | Unresolved question | Closure route |
|---|---|---|
| R6-U01 | Exact Token versus Token Hash runtime roles | BOT official spec or authorized verification |
| R6-U02 | Token/App/Product permission and cardinality | BOT policy/approved account |
| R6-U03 | Expiry, refresh, rotation overlap and revocation propagation | BOT lifecycle documentation/test |
| R6-U04 | BOT audit and admin activity log capabilities | Authorized BOT Portal evidence |
| R6-U05 | Selected private secret store/runner/access-control settings | Future approved architecture and review |
| R6-U06 | Secure egress-enabled worker availability | R4 DNS blocker resolution |
| R6-U07 | TLS/host/redirect behavior in actual worker | Future security implementation tests |
| R6-U08 | Log/CI/Pages canary leak protection | Synthetic test evidence |
| R6-U09 | Account ownership, delegation, offboarding | BOT permission/identity policy |
| R6-U10 | Incident/audit retention and notification rules | Security governance |
| R6-U11 | Cloud manager OIDC versus BOT direct OIDC support | Distinct provider evidence |
| R6-U12 | Actual configured GitHub Actions Secrets/Environments | Authorized metadata-only settings inventory |

Preserve Day-01 BOT-U01..BOT-U09, Day-02 D2-AUTH-U01..U11, R5-U01..U10, credential and egress blockers BOT-R3-CRED-01 / BOT-R4-EGRESS-01 and bilingual maintenance risk BOT-R5-MAINT-01.

## 10. QUESTION → METHOD → EVIDENCE → FINDING → CONFIDENCE → UNKNOWN → IMPACT → NEXT

**QUESTION:** How to make a future BOT connector safe without misrepresenting undocumented Token handling?
**METHOD:** Official BOT/GitHub docs, OWASP security guidance, current repo and workflow inspection, no secrets or gateway calls.
**EVIDENCE:** R6-E01..E12, date/URL, exact workflow source commit, no external immutable webpage snapshot.
**FINDING:** BOT requires secret protection and shows approved token path; TOKEN HASH/expiry/rotate remain UNKNOWN. Public repository and Pages form a concrete exposure path. Secret storage, runtime/CI/agent authority and lifecycle acceptance contract are proposed but NOT IMPLEMENTED.
**CONFIDENCE:** HIGH for official statements and observed workflow code; design status for recommended controls; UNKNOWN for actual runtime.
**UNKNOWN:** R6-U01..U12 and inherited research registers.
**IMPACT:** Future release gate must require independent runtime security proof before any production connector.
**NEXT:** Day 02 R7 Contradiction Resolution only, NOT STARTED.

**STOP:** R6 design recorded only; Day-02 Gate NOT ASSESSED, Issue #11 OPEN, implementation HOLD, Day-01 FROZEN unchanged. UNKNOWN ≠ PASS.
