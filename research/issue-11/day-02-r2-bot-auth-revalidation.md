# Issue #11 — Day 02 / R2: BOT Authentication Independent Revalidation

**Project:** Thailand Economic OS
**Release:** V0.2 — Core Data Connectors
**Issue:** #11 — OPEN
**R1 source:** research/issue-11/day-02-r1-bot-auth-discovery.md (preserved)
**Execution date:** 2026-10-08 Asia/Bangkok (authorized early; calendar plan 2026-10-09 remains advisory)
**Status:** R2_REVALIDATION_RECORDED_WITH_CORRECTIONS_AND_UNKNOWNS
**Day-02 Gate:** NOT_ASSESSED | **R3:** NOT_STARTED | **Implementation:** HOLD
**Day-01:** FROZEN v1.1, unchanged

## 1. QUESTION

Independently challenge R1's account → product/plan → application → request → approval → token → Authorization flow. Which parts are supported by current official BOT evidence, which should be corrected, and which remain UNKNOWN?

## 2. METHOD & INDEPENDENCE LIMIT

R2 revisited BOT's live public Portal home, current Manual, Migration Guide, Statistics product page and Terms of Use **from their original BOT domains**; it did not use the R1 narrative as evidence. The four actual BOT manual illustration images were individually inspected for rate, application controls, credential labels and Postman headers.

The Statistics API detail pages were also checked, but public plain-text extraction yielded only their surrounding portal shell. A separate BOT-URL search-indexed extract showed the API Key / Authorization security text. Thus raw dynamic API-spec capture is **NOT** claimed. R2 is an independent **source re-retrieval/claim challenge** within the same assistant workflow; it is NOT a second-agent or independent-human semantic audit.

No account login, secret collection, live positive/negative gateway request, throttling, parser or production connector action took place. Official URL/date/observed claim are retained; immutable official-source snapshots and checksums remain unavailable.

## 3. EVIDENCE INVENTORY

| Ref | BOT official URL | Authority / evidence observed 2026-10-08 |
|---|---|---|
| E01 | https://portal.api.bot.or.th/ | Current Developer Portal, new gateway and Authorization header, old user re-registration |
| E02 | https://portal.api.bot.or.th/manual | §§1–3: sign-up/email verification, product/plan/cart/app selection, Submit Request, Approved Access, Token copy, Authorization |
| E03 | https://portal.api.bot.or.th/migration | New API Key request, legacy X-IBM-Client-Id and old gateway replaced by Authorization and gateway.api.bot.or.th |
| E04 | https://portal.api.bot.or.th/portal/catalogue-products/statistics-1 | Current display: Statistics Plan, unlimited quota, 2,000 calls per 1 hour; categorylist/observations/search-series |
| E05 | https://portal.api.bot.or.th/portal/catalogue-products/statistics-1/e2dcfd41460e49a86276db01aeb3cd1f/docs | Search-indexed BOT excerpt: Observations v1.0.3, API Key in Authorization, illustrative value 123 (direct body dynamically rendered) |
| E06 | https://portal.api.bot.or.th/portal/catalogue-products/statistics-1/e581631f50164ffc72525b11050b5744/docs | Search-indexed BOT excerpt: Search Stat APIs v1.0.0, same API Key in Authorization (direct body dynamically rendered) |
| E07 | https://portal.api.bot.or.th/assets/images/manual/Illustration%207-1.png | Actual cart screenshot; Statistics Plan 1,000 calls/minute |
| E08 | https://portal.api.bot.or.th/assets/images/manual/Illustration%207-2.png | Actual app screen: Create a new app / Existing app; container for one or multiple credential sets; optional Redirect URLs |
| E09 | https://portal.api.bot.or.th/assets/images/manual/Illustration%209.png | Actual app details screenshot: Approved/Pending access, APP ID, TOKEN, TOKEN HASH, Expires Never, authToken, Rotate/Revoke, 1,000/minute |
| E10 | https://portal.api.bot.or.th/assets/images/manual/Illustration%2010-1.png | Actual Postman screenshot: Authorization with new BOT portal token placeholder |
| E11 | https://portal.api.bot.or.th/terms | BOT API Terms of Use §§4,6,9: service outages, secure access means, provider rights to change limits/discontinue |

## 4. R1 CLAIM-BY-CLAIM REVALIDATION

| R1 claim | R2 decision | Evidence / scope |
|---|---|---|
| New portal Account uses sign-up + email verification; legacy users re-register | **CONFIRMED** | E01 + E02; registration != product approval |
| Product catalogue and Statistics Plan subscription option exist | **CONFIRMED** | E02 + E04; product contains 3 listed Statistics APIs |
| 'Access with this plan' immediately grants access | **CORRECTED / NOT TRUE** | E02 §2.6 states cart choice is **not yet approved**; request is pending |
| User creates/selects Application and submits request | **CONFIRMED** | E02 §§2.7–2.12 + E08 |
| 'Existing App' necessarily reuses token, product rights or app ownership | **STILL UNKNOWN** | E02 §2.9 Thai prose about creating a new app using prior name is ambiguous versus 'Existing app' button in E08; no entitlement cardinality proved |
| An app may contain one or several credential sets | **CONFIRMED AS SCREENSHOT WORDING ONLY** | E08 states this; how real credential reuse/scopes work UNKNOWN; future ownership capability not present-current proof |
| Only after Approved Access is hidden Token visible | **CONFIRMED AS DOCUMENTED FLOW** | E02 §§3.4–3.6 + E09; approval criteria/time/account state UNKNOWN |
| Copy Token to make API request | **CONFIRMED AS DOCUMENTED ACTION** | E02 §3.6 + E10; not a real access test |
| TOKEN, TOKEN HASH and APP ID are interchangeable | **CORRECTED — DO NOT EQUATE** | E09 has **three distinct named fields**. TOKEN is described in UI as application identifier; TOKEN HASH as password for app/auth server. Their cryptographic roles remain UNKNOWN |
| Header is Authorization, new gateway is gateway.api.bot.or.th | **CONFIRMED** | E01 + E02 + E03 independently agree; replaces old X-IBM-Client-Id |
| Statistics security type/API Key; example header Authorization: 123; no Bearer shown | **CONFIRMED WITH DYNAMIC SPEC CAVEAT** | E05/E06 BOT-URL indexed text; E02/E10 directly corroborate raw token placeholder. No evidence that server rejects Bearer or accepts any specific live credential |
| Product currently advertises 2,000 calls/hour and unlimited quota | **CONFIRMED AS DISPLAY** | E04; enforcement scope and 429/Retry-After remain UNKNOWN |
| Manual screenshots show 1,000 calls/minute | **CONFIRMED AS SCREENSHOT DISPLAY; CONFLICT CAUSE STILL UNKNOWN** | E07/E09 conflict with E04; screenshots unversioned; cannot assert which configuration is actually enforced |
| Tokens universally never expire | **STILL UNKNOWN** | E09 says EXPIRES: Never for an illustrative credential; not platform-wide policy |
| BOT terms require access credential protection and permit future limit/service changes | **NEW FINDING** | E11, Terms 6/9; does not prove current error status codes |

## 5. MATERIAL CORRECTIONS AND CONFLICT RESOLUTION BOUNDARIES

**R2-C01 — Existing App semantics: CORRECTED / unresolved.**
The Manual's Thai explanation of 'Existing App' says to create a new Application using a prior application's name with a separate Product, while the UI directly offers an 'Existing app' choice. R1 correctly flagged insufficient detail; R2 explicitly records the internal terminology inconsistency. Neither text proves credential reuse, app-product scope, duplicated credentials or same-token entitlement.

**R2-C02 — Rate display disagreement: STILL UNKNOWN cause.**
E07/E09 illustrate Statistics rate **1,000/minute**, E04 currently lists **2,000/hour** with unlimited quota. The **current product page** is stronger evidence for the *present advertised setting*, not empirical enforcement. Possible documentation vintage or configuration/scope difference is an **unconfirmed hypothesis**. Reserve BOT-U06 for R5; formal contradiction disposition belongs to R7. Do not declare screenshot obsolete as a fact.

**R2-C03 — Credential field semantics: CORRECTED boundaries.**
E09 separately labels:
- APP ID — internal app identifier;
- TOKEN — UI calls this a unique ID identifying the application, with Copy control;
- TOKEN HASH — UI calls this a unique password for app/auth server;
- AUTH METHOD — authToken; ROTATE/REVOKE controls visible; EXPIRES: Never in example.

E02 and E10 instruct users to copy **Token** to Authorization. The UI label description does **not** prove Token Hash is on-wire, nor that Token is safely public. Treat all potential credentials as sensitive. Do not infer actual expiration or rotation semantics from screenshots.

**R2-C04 — Spec extraction limitation: new caveat.**
Direct E05/E06 public HTML extraction only returned the page shell. Search-indexed BOT-source text still shows API Key in header Authorization with sample 'Authorization: 123'. Official Manual and Migration independently affirm the header. Source-specific exported specification URL, version history, binary checksum, and raw immutable capture are **UNKNOWN** (BOT-U07).

**R2-C05 — 'Subscribe' is request-stage terminology, not approval: CORRECTED.**
Manual §2.6 explicitly says the added-to-cart product is not yet approved. The documented transition through Submit Request / Approved Access must not be compressed into a single login or subscription success.

## 6. NEW FINDING: OFFICIAL TERMS (NOT IMPLEMENTATION)

BOT terms §6 requires users to keep access means confidential. §9 reserves BOT's right to revise terms, impose limitations or discontinue API service; §4 discusses computer/network outages.

**Authority:** published policy. **Impact:** future secret management and operations must anticipate provider-controlled changes. **Not proven:** response codes, Retry-After, maintenance schedule, live revocation effects, actual token lifetime. R6 retains security model scope.

## 7. DOCUMENTED FLOW (NOT LIVE-TESTED)

    Developer Account (portal identity / sign-up)
      → Statistics Product + selected Plan
      → Added to cart (NOT APPROVED)
      → Select/Create Application (Existing app behavior not proved)
      → Submit Request
      → Approved Access (when granted)
      → My apps / Token copy (Token Hash distinct)
      → gateway.api.bot.or.th / API-specific listen path
      → Authorization: <BOT_PORTAL_TOKEN> (documented example only)

Do not assume: OAuth2, JWT, a Bearer prefix requirement or rejection, a product-global token, automatic approval, one token covering all products, a universally permanent token, app ownership transfer, account-wide rate enforcement, gateway behavior, or HTTP error taxonomy.

## 8. R1 OPEN UNKNOWN REGISTER AFTER R2

| R1 ID | R2 disposition | Closure direction |
|---|---|---|
| D2-AUTH-U01 approval criteria/latency/rejection | **STILL UNKNOWN** | Official BOT policy or real approved account evidence later |
| D2-AUTH-U02 TOKEN vs TOKEN HASH behavior | **STILL UNKNOWN (documented copy path clarified)** | R3 with legitimate credential, R6 security |
| D2-AUTH-U03 app/credential/product cardinality | **STILL UNKNOWN** | BOT clarification/authorized account UI |
| D2-AUTH-U04 token scope and multi-product access | **STILL UNKNOWN** | Official permission contract / authorized evidence |
| D2-AUTH-U05 expiration/rotation/revocation | **STILL UNKNOWN** | R6; cannot generalize illustrative Never |
| D2-AUTH-U06 account roles/ownership/delegation | **STILL UNKNOWN** | Separate BOT permission/ownership evidence |
| D2-AUTH-U07 real direct-token Authorization success | **NOT TESTED** | R3 only, legitimately usable credential required |
| D2-AUTH-U08 screenshot vs product rate conflict cause | **STILL UNKNOWN** | R5/R7; BOT-U06 open |
| D2-AUTH-U09 API spec stable export/changelog | **STILL UNKNOWN** | BOT-U07 targeted later |
| D2-AUTH-U10 special institution approval requirement | **STILL UNKNOWN** | Specific eligibility policy; generic ToS insufficient |
| D2-AUTH-U11 actual gateway status/headers/latency | **NOT TESTED** | R3/R4 only |

**Carry forward all Day-01 BOT-U01..BOT-U09 without alteration**, especially BOT-U06 and BOT-U07. This work does not prove anything about PCI series code, observations payload schema or API↔BTWS mapping.

## 9. RESEARCH QUALITY / AUDIT LIMITATIONS

- R2 independently revisited primary public sources, but it was **not reviewed by an independent human or separate agent**.
- Directly readable portal, manual and terms claims are HIGH confidence *as published*. Indexed dynamic spec claims have MEDIUM confidence for literal details.
- BOT-hosted screenshots are illustrative historical UI, not current live configuration or verified entitlement for this project.
- URL/date/claim references exist; **immutable raw snapshots/checksums of external BOT pages are not preserved** by this R2.
- No credential tested; approval, permission, 401/403/429 and other statuses remain UNKNOWN.
- R2's completion is methodological evidence checking, NOT Day-02 Gate PASS or BOT connector readiness.

## 10. QUESTION → METHOD → EVIDENCE → FINDING → CONFIDENCE → UNKNOWN → IMPACT → NEXT QUESTION

**QUESTION:** Which R1 auth statements survive an independent official-source challenge?
**METHOD:** fresh direct BOT official pages, actual manual illustration images and BOT-source indexed API doc excerpts; no live API tests.
**EVIDENCE:** E01..E11 with authority/caveats above, retrieved 2026-10-08.
**FINDING:** Core account → Product/Plan → Application → request → approval → Token → Authorization documentary sequence corroborated; Existing App and credential scope unresolved, Token/Hash separated, conflicting rate displays proven; Terms adds provider-rights/secret-protection finding.
**CONFIDENCE:** HIGH for Manual/Portal/Terms, MEDIUM for indexed dynamic API text; LIVE behavior UNKNOWN.
**UNKNOWN:** D2-AUTH-U01..U11 and BOT-U01..U09 all remain explicit.
**IMPACT:** No app/credential/quotas assumptions can be promoted into production connectors.
**NEXT QUESTION:** R3, subject to a legitimate usable BOT credential: can a **single safe positive request** demonstrate authentication without exposing a secret? If no legitimate credential, mark DOCUMENTED AUTH = PASS / LIVE AUTH TEST = BLOCKED, never manufacture 200 OK.

## 11. STOP BOUNDARY

- Day 1 FROZEN v1.1 / Gate PASS: UNCHANGED.
- Day 2 R1: RECORDED and historical artifact preserved.
- **Day 2 R2: REVALIDATION RECORDED WITH CORRECTIONS & UNKNOWNS.**
- Day 2 R3: NOT STARTED. R4–R8: NOT STARTED.
- Day-02 Gate: NOT ASSESSED.
- Issue #11: OPEN; production connector: HOLD.

**UNKNOWN ≠ PASS.**
