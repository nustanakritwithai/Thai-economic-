# Issue #11 — Day 02 / R1: BOT Authentication Discovery

**Project:** Thailand Economic OS / V0.2 Core Data Connectors
**Issue:** #11 — Inventory official P0 data endpoints
**Round:** Day 02, R1 — Authentication Discovery
**Originally planned calendar date:** 2026-10-09
**Actual execution date:** 2026-10-08 (Asia/Bangkok; explicit handoff authorization)
**Status:** R1_DISCOVERY_RECORDED / R2_NOT_STARTED
**Day-02 Gate:** NOT ASSESSED
**Production connector:** HOLD
**Precondition:** Day-01 FROZEN v1.1 / Gate PASS (unchanged)
**R1 live authenticated / unauthorized API tests:** NONE; tests belong to R3/R4

## 1. QUESTION

What is the precise **currently documented** relationship between BOT Developer Account, Statistics Product/Plan subscription, Application, Access Request, Approved Access, Token, and HTTP Authorization header? Which parts remain UNKNOWN?

## 2. METHOD

Read the Frozen Day-01 baseline, Day-02 plan, open Issue #11, and the Bank of Thailand's **current official** Developer Portal, Manual (including screenshots), Migration Guide and Statistics Product/API documentation. Compare admin-flow wording with screenshots and the current product page. Preserve negative findings as UNKNOWN rather than treating silence as evidence of absence.

No BOT login, credential acquisition, live gateway request, error probe, throttle test, parser, deployment, or connector implementation was attempted. Evidence preservation is URL + observation date; immutable external webpage captures/checksums have **not** been established in R1.

## 3. OFFICIAL EVIDENCE INVENTORY

| ID | BOT official source | Relevance | Verified |
|---|---|---|---|
| D2-E01 | https://portal.api.bot.or.th/ | New platform, gateway, auth header, new account | 2026-10-08 |
| D2-E02 | https://portal.api.bot.or.th/manual | Registration, shopping-cart access request, application setup, approved token, Postman example | 2026-10-08 |
| D2-E03 | https://portal.api.bot.or.th/migration | Legacy-to-current header, gateway, credentials | 2026-10-08 |
| D2-E04 | https://portal.api.bot.or.th/portal/catalogue-products/statistics-1 | Statistics Product/Plan, current listed rate, Auth Token | 2026-10-08 |
| D2-E05 | https://portal.api.bot.or.th/portal/catalogue-products/statistics-1/e2dcfd41460e49a86276db01aeb3cd1f/docs | Statistics Observations contract: API Key in Authorization | 2026-10-08 |
| D2-E06 | https://portal.api.bot.or.th/portal/catalogue-products/statistics-1/e581631f50164ffc72525b11050b5744/docs | Statistics Search series API Key in Authorization | 2026-10-08 |
| D2-E07 | https://portal.api.bot.or.th/assets/images/manual/Illustration%207-1.png | Screenshot: Selected Products and Selected Plan | 2026-10-08 |
| D2-E08 | https://portal.api.bot.or.th/assets/images/manual/Illustration%207-2.png | Screenshot: new/existing app selection; app described as credential container | 2026-10-08 |
| D2-E09 | https://portal.api.bot.or.th/assets/images/manual/Illustration%209.png | Screenshot: app ID, Approved/Pending tabs, TOKEN vs TOKEN HASH, ROTATE/REVOKE, authToken | 2026-10-08 |
| D2-E10 | https://portal.api.bot.or.th/assets/images/manual/Illustration%2010-1.png | Screenshot: Authorization header carrying portal Token placeholder | 2026-10-08 |

**Source caveat:** Some API-spec pages are dynamically rendered; contract language in D2-E05/E06 was corroborated in current search-indexed BOT page excerpts. R1 did not preserve a raw spec export or proof of spec history (BOT-U07 remains UNKNOWN). A Manual screenshot is an illustrative example, not a live entitlement/configuration snapshot.

## 4. DIRECTLY DOCUMENTED ACCOUNT → TOKEN RELATIONSHIPS

| Layer | Documented finding | Classification and confidence | Evidence |
|---|---|---|---|
| **Account** | A user creates a current BOT Developer Portal account with email verification and profile/password. The new system requires re-registration of old-system users. Account registration alone is not documented as API Product approval. | DOCUMENTED FACT / HIGH | E01, E02 |
| **Product** | Logged-in user goes to Catalogues, selects a Product such as Statistics. The Statistics Product groups categorylist, observations and search-series. | DOCUMENTED FACT / HIGH | E02, E04 |
| **Plan** | Select Overview → Access with this plan. Product/Plan selection places the item in a cart; its 'Success' notification means **added to cart**, not approved access. | DOCUMENTED FACT / HIGH | E02, E07 |
| **Application** | Cart has Selected Products, Selected Plan and 'Create a new app' / 'Existing App'. For a new app it requests App Name and Description. Screenshot describes an app as a container of one or multiple credential sets. | DOCUMENTED FACT + UI EXAMPLE / HIGH | E02, E08 |
| **Request** | Submit Request sends the selected plan/product/application access request. Approval is a separate stage. | DOCUMENTED FACT / HIGH | E02 |
| **Approved Access** | User opens Profile → My apps → chosen Application. Manual says the hidden Token becomes visible **after Approved Access**. Example UI distinguishes Approved access / Pending access. | DOCUMENTED FACT / HIGH | E02, E09 |
| **Token** | Manual instructs user to copy the **TOKEN** field in the Application credential view. The example separately displays TOKEN HASH, EXPIRES, auth method authToken and ROTATE/REVOKE. | DOCUMENTED FACT for copy action; illustrative UI for the other labels / HIGH | E02, E09 |
| **Gateway/Header** | Current gateway: https://gateway.api.bot.or.th/. Migration Guide replaces old X-IBM-Client-Id with **Authorization**. Statistics API docs call security 'API Key' and say put the token in header Authorization; sample: 'Authorization: 123'. | DOCUMENTED FACT / HIGH for published contract; live behavior UNTESTED | E01, E03, E05, E06, E10 |

### Current documented relationship (not a live-tested sequence)

~~~text
Developer Account (identity; email verified)
  → Catalogue: Statistics Product → Statistics Plan
  → Cart / Selected Products + Selected Plan
  → Create or choose Application
  → Submit Request (NOT the same as approval)
  → Approved Access for the app/product request
  → My apps → App Credential → Copy Token
  → HTTP request to new Gateway with Authorization header
~~~

### Published request-shape illustration only

~~~http
GET https://gateway.api.bot.or.th/<API-specific-listen-path>
Authorization: <NEW_BOT_PORTAL_TOKEN>
~~~

Current Statistics docs show **Authorization: 123** as an illustrative example; **123 is not a credential**. A 'Bearer ' prefix is **not shown** in these examined BOT examples. This is documented syntax evidence, not a tested guarantee of acceptance. Whether the Token Hash has any separate required runtime role remains UNKNOWN.

## 5. INDEPENDENT QUESTIONS & APPARENT CONFLICTS LOGGED FOR R2

**D2-R1-C01 — Manual image vs current Statistics rate.**
The Manual's illustrative Selected Plan / Approved-access screenshots show **1,000 calls / 1 minute**. The current Product listing shows **2,000 calls / 1 hour; quota unlimited**. Classification: **DOC_FRESHNESS_OR_CONFIG_DIFFERENCE — UNRESOLVED**. R1 prefers the explicitly current Product listing as a *documented current display*, not proof of live enforcement. Do **not** close BOT-U06; enforcement belongs to R5. Evidence: E04, E07, E09.

**D2-R1-C02 — Application reuse wording.**
The Manual's explanation of 'Existing App' is not precise enough to establish whether selecting it reuses an existing credential, adds a product entitlement, or changes credential count. UI says app may contain one or multiple credential sets. Classification: **UI_TERMINOLOGY / SCOPING UNKNOWN**. Evidence: E02, E08.

**D2-R1-C03 — TOKEN versus TOKEN HASH.**
Manual's numbered Copy action is adjacent to TOKEN, but screenshot also displays a separate TOKEN HASH described as a password for app/auth server. R1 does not equate the two, does not assert Hash is a header value, and treats both as sensitive. Classification: **DOCUMENTED HEADER PATH / OTHER CREDENTIAL SEMANTICS UNKNOWN**. Evidence: E02, E09, E10.

**D2-R1-C04 — Account vs app vs product entitlement.**
A signed-in account, a selected plan, an app, and an approved credential are different objects. Actual many-to-many cardinality and permissions scope cannot be inferred from the illustrative screenshot. Classification: **DOCUMENTED RELATIONSHIP / CARDINALITY UNKNOWN**.

## 6. OPEN R1 UNKNOWN REGISTER

| ID | Question | Status | Closure direction |
|---|---|---|---|
| D2-AUTH-U01 | Approval criteria, approval latency, rejection status? | UNKNOWN | R2 official policy / later authorized portal evidence |
| D2-AUTH-U02 | Exact TOKEN vs TOKEN HASH semantics and which field is used in every auth mode? | PARTIAL; beyond Manual's Token copy UNKNOWN | R2, later R3 only if lawful credential |
| D2-AUTH-U03 | App/product/subscription/credential cardinality; reuse of Existing App? | UNKNOWN | R2 docs; later approved UI |
| D2-AUTH-U04 | Token scope per account, app, product or credential set? Multi-product access? | UNKNOWN | R2 official policy, later controlled evidence |
| D2-AUTH-U05 | Expiry, renewal, rotation and revoke behavior for live credentials? | UNKNOWN | R2/R6; screenshot 'Never' is illustrative |
| D2-AUTH-U06 | Account roles, app ownership transfer and delegated user permissions? | UNKNOWN | R2 or later official account policy |
| D2-AUTH-U07 | Live acceptance of direct-token header, optional formatting and client requirements? | UNTESTED | R3 legitimate credential only |
| D2-AUTH-U08 | Explanation/currentness of conflicting Manual screenshot and Product Plan rates? | UNRESOLVED | R2 freshness check; R5 scope/enforcement |
| D2-AUTH-U09 | Stable downloadable API spec URL/changelog/history? | BOT-U07 UNKNOWN | targeted later official-spec inspection |
| D2-AUTH-U10 | Institution-level verification required for Statistics subscription? | UNKNOWN | R2 current official terms |
| D2-AUTH-U11 | Status/content-type/latency and HTTP error taxonomy for live gateway? | NOT TESTED | R3/R4 only, no R1 probes |

**Carry forward all Day-01 BOT-U01..BOT-U09 unchanged.** In particular, BOT-U06 (live rate enforcement scope) and BOT-U07 (spec export history) are NOT closed.

## 7. IMPACT / NON-IMPLEMENTATION GUARDRAILS

1. **Do not collapse** Developer Account, Product/Plan, Application, approved entitlement, and Token into one object. Exact relationship cardinality requires proof.
2. Never put Token **or** Token Hash in repo/README/Issue/CI output/log/screenshot/exception/URL. Future secret injection via Secret Store/Environment is a design recommendation for R6, not an implemented control.
3. Do not assume OAuth/JWT, Bearer prefix, refresh-token flow, universal app-scoped quota, fixed lifetime or HTTP status taxonomy from R1 evidence.
4. Documented current config is not live-tested rate enforcement, token validation, or permission behavior.
5. No production schema migration, request client, parser, retry engine, DB or policy agent is authorized by this round.

## 8. QUESTION / METHOD / EVIDENCE / FINDING / CONFIDENCE / UNKNOWN / IMPACT / NEXT QUESTION

- **QUESTION:** exact current account→product/plan→application→access request→approval→token→Authorization relationship.
- **METHOD:** targeted BOT official documentation plus official illustrative images; no live gateway or secret use.
- **EVIDENCE:** D2-E01..E10, dates, URL provenance and caveats above.
- **FINDING:** documented admin authentication sequence and published header syntax established; app credential view distinguishes Token/Token Hash; stale Manual rate illustration detected.
- **CONFIDENCE:** HIGH for direct published flow/header; LOW or UNKNOWN for live behavior, credential cardinality/expiry and approval mechanics.
- **UNKNOWN:** D2-AUTH-U01..U11; all Day-1 critical unknowns retained.
- **IMPACT:** safe future credential/entitlement boundaries; still no connector authorization.
- **NEXT QUESTION:** Can an independent R2 revalidation confirm/correct each step and resolve the screenshot/credential ambiguities without guessing?

## 9. ROUND END / STOP BOUNDARY

- **R1:** RECORDED — documentation discovery only, not independent semantic certification.
- **R2:** NOT STARTED. Next exact round = independent revalidation; do **not** advance during this R1 work block.
- **R3/R4:** NOT STARTED; no credential or HTTP observations available in this round.
- **R5–R8:** NOT STARTED.
- **Day-02 Gate:** NOT ASSESSED.
- **Issue #11:** OPEN.
- **V0.2 connector implementation:** HOLD.
- **Day 1 Frozen v1.1:** preserved without amendments.

**UNKNOWN ≠ PASS.**
