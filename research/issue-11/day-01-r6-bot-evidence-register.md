# Issue #11 — Day 01 Round 6
## BOT Evidence Hardening Register

**Date:** 2026-10-08  
**Parent:** Day 01 — BOT Data Ecosystem Map  
**Round:** R6 — Evidence Hardening  
**Inputs:** R1–R5  
**Goal:** Convert critical BOT conclusions into auditable claims with explicit evidence, authority scope, confidence, caveats, and invalidation conditions.

---

# REGISTER RULES

Each claim records:

- **Claim ID**
- **Statement**
- **Classification**
- **Authority scope**
- **Official evidence**
- **Evidence date**
- **Confidence**
- **Caveat**
- **Invalidation condition**
- **Design impact**

Classification:
- **FACT** — directly supported by current official BOT evidence.
- **SUPPORTED DESIGN** — design conclusion supported by evidence but not itself a BOT-published fact.
- **UNKNOWN** — deliberately unresolved.
- **NEGATIVE FINDING** — no authoritative relationship found after targeted search; not proof of nonexistence.

---

## BOT-CLM-001 — Current BOT API portal/gateway/header

**Statement**  
The current BOT API platform uses:
- Developer Portal: `https://portal.api.bot.or.th/`
- Gateway: `https://gateway.api.bot.or.th/`
- Authorization header: `Authorization`

The new platform has been in use since 17 September 2025.

**Classification:** FACT  
**Authority scope:** current BOT API platform / migration state  
**Evidence:**
- https://portal.api.bot.or.th/
- https://portal.api.bot.or.th/migration
**Evidence date:** 2026-10-08  
**Confidence:** HIGH  
**Caveat:** Current-state claim; future migration may supersede it.  
**Invalidation condition:** BOT publishes a newer migration/current gateway/header.  
**Design impact:** connector config must not hard-code legacy `apigw1.bot.or.th` / `X-IBM-Client-Id`.

---

## BOT-CLM-002 — Statistics is a distinct BOT API Product

**Statement**  
The current Statistics Product exposes:
- `/categorylist`
- `/observations`
- `/search-series`

The current Statistics Plan shows:
- quota: unlimited
- rate: 2,000 calls / 1 hour.

**Classification:** FACT  
**Authority scope:** Statistics Product contract/config  
**Evidence:**  
https://portal.api.bot.or.th/portal/catalogue-products/statistics-1
**Evidence date:** 2026-10-08  
**Confidence:** HIGH  
**Caveat:** Product configuration may change.  
**Invalidation condition:** Statistics Product page changes API family/plan/rate.  
**Design impact:** Statistics must be represented as a product-level configuration boundary.

---

## BOT-CLM-003 — search-series is the official Statistics discovery interface

**Statement**  
`search-series` is an official Statistics API used to search by:
- series code;
- series name;
- keyword/relevant term;

with up to 100 series returned per search.

**Classification:** FACT  
**Authority scope:** series discovery  
**Evidence:**  
https://portal.api.bot.or.th/portal/catalogue-products/statistics-1/e581631f50164ffc72525b11050b5744/docs
**Observed API version:** v1.0.0  
**Base URL:** https://gateway.api.bot.or.th/search-series  
**Evidence date:** 2026-10-08  
**Confidence:** HIGH  
**Caveat:** Exact response fields/live behavior remain later research.  
**Invalidation condition:** BOT changes the API contract/version or deprecates the endpoint.  
**Design impact:** exact provider series codes must be discovered, never inferred from BTWS identifiers.

---

## BOT-CLM-004 — observations retrieves Statistics values by series code

**Statement**  
The Statistics `observations` API filters observations using a BOT series code.

The official documentation states the series code can be obtained from a downloadable **List of Statistics APIs**.

**Classification:** FACT  
**Authority scope:** machine observation retrieval / discovery dependency  
**Evidence:**  
https://portal.api.bot.or.th/portal/catalogue-products/statistics-1/e2dcfd41460e49a86276db01aeb3cd1f/docs
**Observed API version:** v1.0.3  
**Base URL:** https://gateway.api.bot.or.th/observations  
**Evidence date:** 2026-10-08  
**Confidence:** HIGH  
**Caveat:** direct API-list file URL/schema is still UNKNOWN.  
**Invalidation condition:** Observations contract/version changes.  
**Design impact:** canonical acquisition path is discovery → provider series code → observations.

---

## BOT-CLM-005 — The official List of Statistics APIs exists

**Statement**  
BOT officially exposes a downloadable “List of Statistics APIs” intended to provide Statistics series codes.

**Classification:** FACT for existence / UNKNOWN for file mechanics  
**Authority scope:** Statistics series inventory  
**Evidence:** Observations documentation above  
**Evidence date:** 2026-10-08  
**Confidence:** HIGH for existence  
**Caveat:** direct URL, file type, schema, versioning, archive behavior are UNKNOWN.  
**Invalidation condition:** BOT removes/replaces the list.  
**Design impact:** candidate registry-bootstrap artifact; do not operationalize until inspected.

---

## BOT-CLM-006 — Application/subscription/token workflow

**Statement**  
The current BOT API onboarding flow includes:
1. create account;
2. select Product/Plan;
3. subscribe/request access;
4. create/select Application;
5. submit request;
6. after Approved Access, Token becomes visible;
7. send the Token in `Authorization`.

The manual shows 200 OK as a successful example and exposes Dashboard Performance/Error views with CSV export.

**Classification:** FACT  
**Authority scope:** authentication administration / operational telemetry  
**Evidence:**  
https://portal.api.bot.or.th/manual
**Evidence date:** 2026-10-08  
**Confidence:** HIGH  
**Caveat:** live failure status/body behavior is still Day-2 work.  
**Invalidation condition:** BOT changes credential/subscription workflow.  
**Design impact:** secret/token is application-scoped credential material; do not store in repository.

---

## BOT-CLM-007 — Product-level rate configuration differs across BOT

**Statement**  
Rate limits are not safely modeled as one BOT-wide constant.

Current official product pages show:
- Statistics: 2,000 calls/hour
- Exchange Rates: 200 calls/hour
- Interest Rates: 200 calls/hour

**Classification:** FACT  
**Authority scope:** current product plan configuration  
**Evidence:**
- Statistics: https://portal.api.bot.or.th/portal/catalogue-products/statistics-1
- Exchange Rates: https://portal.api.bot.or.th/portal/catalogue-products/exchange-rates-1
- Interest Rates: https://portal.api.bot.or.th/portal/catalogue-products/interest-rates-1
**Evidence date:** 2026-10-08  
**Confidence:** HIGH  
**Caveat:** enforcement scope (per token/app/account/product) remains UNKNOWN.  
**Invalidation condition:** product plans/rates change.  
**Design impact:** rate-limit config belongs at product/API configuration level.

---

## BOT-CLM-008 — API versions are per API, not one Statistics-wide version

**Statement**  
Current Statistics APIs do not share one universal version:
- search-series: v1.0.0
- observations: v1.0.3

**Classification:** FACT  
**Authority scope:** API specification identity  
**Evidence:** official API documentation pages  
**Evidence date:** 2026-10-08  
**Confidence:** HIGH  
**Caveat:** no public historical changelog/archive has yet been confirmed.  
**Invalidation condition:** specs are revised.  
**Design impact:** preserve API name + spec version + retrieval date/spec checksum.

---

## BOT-CLM-009 — BOT Statistics website is a separate publication/dissemination surface

**Statement**  
BOT maintains a Statistics and Dissemination website with domain-specific statistical sections including:
- Financial Market
- Monetary Statistics
- Financial Institutions
- Payment
- External Sector
- Fiscal Sector
- Real Sector
- Economic and Financial Index and Indicators
- Regional statistics

**Classification:** FACT  
**Authority scope:** public statistics dissemination/navigation  
**Evidence:**  
https://www.bot.or.th/en/statistics.html
**Evidence date:** 2026-10-08  
**Confidence:** HIGH  
**Caveat:** this surface is not itself the API contract.  
**Invalidation condition:** BOT restructures statistics publication pages.  
**Design impact:** publication/navigation and API access must remain separate concepts.

---

## BOT-CLM-010 — Official BOT navigation can contain stale legacy API links

**Statement**  
The current BOT Statistics page still exposes a BOT API link pointing to the legacy `apiportal.bot.or.th/bot/public` location while the current BOT API platform is `portal.api.bot.or.th` / `gateway.api.bot.or.th`.

**Classification:** FACT  
**Authority scope:** navigation freshness risk  
**Evidence:**
- https://www.bot.or.th/en/statistics.html
- https://portal.api.bot.or.th/
**Evidence date:** 2026-10-08  
**Confidence:** HIGH  
**Caveat:** the stale link may be corrected at any time.  
**Invalidation condition:** BOT updates the Statistics navigation link.  
**Design impact:** official-domain provenance must be paired with canonical-current URL verification and `last_verified`.

---

## BOT-CLM-011 — BOT publishes explicit table/report lifecycle changes

**Statement**  
BOT publishes a revised-table list that maps Previous Report ID/Name to New Report ID/Name with publication/data dates.

Example mappings include identifiers such as:
- `EC_MB_033_S3 → EC_MB_033_S4`
- `FM_RT_001_S2 → FM_RT_001_S3`

**Classification:** FACT  
**Authority scope:** publication table/report lifecycle  
**Evidence:**  
https://www.bot.or.th/en/statistics/revised-table-list.html
**Evidence date:** 2026-10-08  
**Confidence:** HIGH  
**Caveat:** this proves table/report lifecycle, **not API series-code lifecycle**.  
**Invalidation condition:** lifecycle publication is withdrawn or semantics change.  
**Design impact:** external publication identifiers require supersession relationships; do not overwrite identity.

---

## BOT-CLM-012 — API series lifecycle is not proven by revised-table evidence

**Statement**  
No evidence currently establishes that API `series_code` follows the same replacement/discontinuation lifecycle as BOT publication table/report identifiers.

**Classification:** NEGATIVE FINDING / UNKNOWN  
**Authority scope:** cross-surface lifecycle mapping  
**Evidence basis:** targeted R2–R6 review of current Statistics API and publication lifecycle surfaces  
**Evidence date:** 2026-10-08  
**Confidence:** HIGH that it is **not yet proven**, not that no mapping exists.  
**Caveat:** absence of found evidence is not proof of absence.  
**Invalidation condition:** official BOT documentation/API list explicitly maps API series lifecycle to table/report lifecycle.  
**Design impact:** do not manufacture `series_code` supersession from revised-table records.

---

## BOT-CLM-013 — BTWS table code and URL report_id are distinct identifier namespaces

**Statement**  
For the inspected Private Consumption table:
- the BTWS page title identifies table code `EC_EI_003_S3`;
- the page URL uses `reportID=995`.

These are distinct source identifiers.

**Classification:** FACT  
**Authority scope:** publication identity  
**Evidence:**  
https://app.bot.or.th/BTWS_STAT/statistics/BOTWEBSTAT.aspx?language=ENG&reportID=995
**Evidence date:** 2026-10-08  
**Confidence:** HIGH  
**Caveat:** exact report_id semantics across all tables need not be assumed from one example.  
**Invalidation condition:** BOT changes BTWS identifier model.  
**Design impact:** external IDs must carry namespaces: `BOT:table_code`, `BOT:report_id`, `BOT:api_series`.

---

## BOT-CLM-014 — BOT API series ↔ BTWS table/report mapping remains unproven

**Statement**  
No authoritative one-to-one mapping has yet been found between:
- BTWS `table_code`;
- BTWS `report_id`;
- Statistics API `series_code`.

**Classification:** NEGATIVE FINDING / UNKNOWN  
**Authority scope:** cross-surface identity mapping  
**Evidence basis:** targeted searches across API documentation, Statistics website, BTWS and lifecycle pages during R2–R6  
**Evidence date:** 2026-10-08  
**Confidence:** HIGH that the mapping is **not yet evidenced**  
**Caveat:** the downloadable List of Statistics APIs may contain a bridge.  
**Invalidation condition:** an official mapping is found.  
**Design impact:** title/code similarity cannot be used as identity proof.

---

## BOT-CLM-015 — BOT macro concept pages explicitly link concepts to publication tables

**Statement**  
BOT's Economic and Financial Index and Indicators page explicitly maps macro concepts to named BOT tables, e.g.:
- Export/Import/Trade balance → EC_XT_047_S2
- International reserves → EC_XT_030
- Loans to Household → EC_MB_039_S2
- Interest rate → FM_RT_001_S2
- Exchange rate → FM_FX_001_S3

**Classification:** FACT  
**Authority scope:** semantic concept → publication table bridge  
**Evidence:**  
https://www.bot.or.th/en/statistics/economic-and-financial-index-and-indicators.html
**Evidence date:** 2026-10-08  
**Confidence:** HIGH  
**Caveat:** this does not prove API series mapping.  
**Invalidation condition:** BOT changes concept/table mappings.  
**Design impact:** useful semantic-selection evidence for choosing proof datasets and validating canonical concepts.

---

## BOT-CLM-016 — BTWS is suitable as an official human verification surface

**Statement**  
For inspected statistical tables, BTWS exposes official human-readable published values and source/context information suitable for manual cross-check.

**Classification:** SUPPORTED DESIGN  
**Authority scope:** human verification  
**Evidence:**  
https://app.bot.or.th/BTWS_STAT/statistics/BOTWEBSTAT.aspx?language=ENG&reportID=995
**Evidence date:** 2026-10-08  
**Confidence:** HIGH for inspected table  
**Caveat:** “verification surface” is our design role, not BOT terminology. It does not authorize automated fallback.  
**Invalidation condition:** BTWS stops representing current official published data or selected API/table semantics fail to match.  
**Design impact:** use BTWS to cross-check first proof; preserve disagreements instead of silently reconciling them.

---

## BOT-CLM-017 — Official surfaces are question-specific, not interchangeable

**Statement**  
No single BOT surface should be treated as universal authority for acquisition, semantics, lifecycle, verification, and operational state.

**Classification:** SUPPORTED DESIGN  
**Authority scope:** source-role governance  
**Evidence basis:** R1–R5 official-surface mapping  
**Evidence date:** 2026-10-08  
**Confidence:** HIGH  
**Caveat:** this is project architecture, not an official BOT claim.  
**Invalidation condition:** future BOT architecture collapses these functions into one authoritative machine contract with explicit equivalence.  
**Design impact:** agents must select authority based on the question being answered.

---

# CRITICAL UNKNOWN REGISTER

| Unknown ID | Question | Why it matters | Closure route |
|---|---|---|---|
| BOT-U01 | Direct URL/file type/schema of List of Statistics APIs | registry bootstrap | inspect download artifact |
| BOT-U02 | Exact API series code for PCI total | first proof series | Day 3/5 |
| BOT-U03 | Exact observations live response schema | parser contract | Day 4 |
| BOT-U04 | Direct revision/release metadata in observations response | vintage model | Day 6 |
| BOT-U05 | BTWS table/row ↔ API series mapping | cross-check/fallback | API list + series discovery + value/metadata comparison |
| BOT-U06 | Rate-limit enforcement scope | retry/throttle design | Day 2 docs/live evidence |
| BOT-U07 | Stable API spec export URL/history | contract snapshotting | inspect export |
| BOT-U08 | File publication equivalence to API | fallback policy | later source comparison |
| BOT-U09 | API series-code lifecycle | source registry lifecycle | explicit BOT series lifecycle evidence |

UNKNOWN ≠ PASS.

---

# CLAIM STALENESS / REVALIDATION POLICY

Claims should not live forever without re-check.

## Revalidate immediately when
- API returns unexpected status/schema;
- official endpoint redirects or fails;
- product/spec version changes;
- selected proof series disappears;
- BOT publishes migration/maintenance notice affecting interface;
- publication table is revised/replaced/discontinued;
- API and BTWS/file values diverge unexpectedly.

## Scheduled revalidation recommendation
During active V0.2:
- current API-contract claims: re-check before connector implementation and release gate;
- selected source metadata: re-check at proof time;
- lifecycle mappings: re-check if source identifiers change.

---

# R6 QUALITY CHECK

| Requirement | Status |
|---|---|
| Critical current API claims have official evidence | PASS |
| Evidence authority scope is explicit | PASS |
| Fact vs design hypothesis separated | PASS |
| Negative findings labeled as non-proof-of-absence | PASS |
| Confidence recorded | PASS |
| Caveats recorded | PASS |
| Invalidation conditions recorded | PASS |
| Major UNKNOWNs isolated | PASS |
| No UNKNOWN promoted to PASS | PASS |

---

# ROUND-6 RESULT

**Evidence Hardening: PASS**

R6 converts the BOT Day-1 research into an auditable claim register rather than a prose-only understanding.

This does **not** close Day 1.

---

# NEXT ROUND

## Round 7 — Contradiction Resolution

Goal:
Systematically identify and resolve conflicts among the hardened claims/surfaces.

Priority contradiction classes:
1. current vs legacy API navigation;
2. publication table lifecycle vs unknown API-series lifecycle;
3. API vs BTWS/file value/vintage;
4. table_code vs report_id vs series_code identity;
5. API product/version/rate differences;
6. semantic title similarity vs proven mapping.

For each contradiction:
- define both statements;
- identify authority scope;
- decide whether conflict is real or only scope mismatch;
- resolve, or retain explicit UNKNOWN;
- update claim register only with evidence.

---

## Rule

A claim without authority scope is weak evidence.  
A negative search is not proof of nonexistence.  
Every hardened claim must say what would make it stale or false.  
UNKNOWN ≠ PASS.
