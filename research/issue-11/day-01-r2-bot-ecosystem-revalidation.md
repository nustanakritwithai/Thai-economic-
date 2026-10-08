# Issue #11 — Day 01 Round 2
## BOT Ecosystem Independent Revalidation

**Date:** 2026-10-08  
**Parent:** Day 01 — BOT Data Ecosystem Map  
**Round:** R2 — Independent Revalidation  
**Method:** Re-check Day-1 claims independently against current official BOT sources.  
**Rule:** The Day-1 summary is treated as a hypothesis list, not as evidence.

---

## ROUND-2 PURPOSE

Round 1 discovered the BOT ecosystem.

Round 2 asks a different question:

> If we ignore the Day-1 conclusions and independently re-check the official BOT sources, which claims are still true, which are too broad, which remain unknown, and what new evidence appears?

Classification used:
- **CONFIRMED**
- **SUPPORTED / DESIGN HYPOTHESIS**
- **CORRECTED / OVERCLAIMED**
- **STILL UNKNOWN**
- **NEW FINDING**

---

# CLAIM REVALIDATION TABLE

## C01 — The current BOT API system is the new portal/gateway introduced on 17 Sep 2025
**Round-1 claim:** current machine entry point is portal.api.bot.or.th / gateway.api.bot.or.th, available from 17 Sep 2025.

**R2 status:** **CONFIRMED**

Independent evidence:
- BOT API portal states the new system is available from 17 September 2025.
- Developer Portal: https://portal.api.bot.or.th/
- Gateway: https://gateway.api.bot.or.th/
- Existing users must create a new account in the new system.

Official evidence:
https://portal.api.bot.or.th/

---

## C02 — Statistics is a distinct API Product exposing categorylist, observations, search-series
**R2 status:** **CONFIRMED**

Independent evidence:
The current Statistics product lists exactly these REST APIs:
- Stat Category — /categorylist
- Observations — /observations
- search-series — /search-series

It also currently displays:
- quota: unlimited
- rate: 2,000 calls / 1 hour

Official evidence:
https://portal.api.bot.or.th/portal/catalogue-products/statistics-1

---

## C03 — categorylist is a structured browse/discovery mechanism
**R2 status:** **CONFIRMED, WITH LIMITED SCOPE**

Independent evidence:
The Statistics product exposes Stat Category through /categorylist and documentation identifies category/series list operations.

What R2 confirms:
- category-oriented discovery exists.

What R2 does not yet prove:
- exact live request parameters;
- full response fields;
- whether categorylist alone is sufficient for all Statistics discovery.

These details remain scheduled for later API-specific investigation.

---

## C04 — search-series is the official free-text/identifier discovery route
**R2 status:** **CONFIRMED**

Independent evidence:
Official Search Stat APIs documentation states users can search using:
- series code;
- series name;
- relevant terms/keywords.

Each search displays up to 100 series.

Base:
https://gateway.api.bot.or.th/search-series

Official evidence:
https://portal.api.bot.or.th/portal/catalogue-products/statistics-1/e581631f50164ffc72525b11050b5744/docs

Implication:
Exact series identifiers should be discovered from BOT, not guessed from BTWS table names.

---

## C05 — observations retrieves statistical values by series code
**R2 status:** **CONFIRMED**

Independent evidence:
Official Observations documentation states users filter observations by series code.

Base:
https://gateway.api.bot.or.th/observations

The documentation also explicitly mentions a downloadable **List of Statistics APIs** containing series codes.

Official evidence:
https://portal.api.bot.or.th/portal/catalogue-products/statistics-1/e2dcfd41460e49a86276db01aeb3cd1f/docs

### New lead
A downloadable official Statistics API/series list exists.

### Still unknown
- stable direct machine URL for that download;
- its exact schema/format;
- whether it can become a source-registry bootstrap artifact.

This becomes a Gap-Hunt item for Round 3.

---

## C06 — legacy gateway/header differs from the current system
**R2 status:** **CONFIRMED**

Official Migration Guide independently confirms:

Old:
- gateway: https://apigw1.bot.or.th/bot/public
- header: X-IBM-Client-Id

New:
- gateway: https://gateway.api.bot.or.th/
- header: Authorization with a new value/token.

Official evidence:
https://portal.api.bot.or.th/migration

Implication:
Online examples using the old gateway/header are not safe implementation references without reconciliation.

---

## C07 — Developer Portal also controls subscription/application credentials
**R2 status:** **CONFIRMED**

Official manual independently documents:
1. create account;
2. choose catalogue/product;
3. subscribe to plan;
4. create/select application;
5. submit request;
6. after Approved Access, token becomes visible;
7. use token in Authorization header.

The manual also documents Dashboard → Performance and error reporting/export.

Official evidence:
https://portal.api.bot.or.th/manual

Detailed authentication behavior remains Day 2; Round 2 only confirms the portal's ecosystem role.

---

## C08 — BOT public Statistics site is a separate official statistics/publication surface
**R2 status:** **CONFIRMED**

Independent evidence:
https://www.bot.or.th/en/statistics.html

It provides:
- statistics domains;
- BOT API navigation;
- general publication schedule;
- discontinued-series/table resources;
- table-level statistical access.

General schedule shown:
- daily: every business day;
- weekly: last business day of following week;
- monthly: last business day of following month unless otherwise specified;
- quarterly: last business day of following quarter unless otherwise specified;
- yearly: last business day of following year unless otherwise specified.

Individual table metadata may override/generalize this.

---

## C09 — BTWS is an official human-readable statistics and metadata surface
**R2 status:** **CONFIRMED**

Independent PCI table evidence:
https://app.bot.or.th/BTWS_STAT/statistics/BOTWEBSTAT.aspx?language=ENG&reportID=995

The official table exposes:
- human-readable observations;
- reporting range;
- Last Updated;
- unit/base;
- Download;
- Metadata;
- p/r status markers.

This confirms its usefulness as an official verification surface.

---

## C10 — PCI has explicit revision behavior
**R2 status:** **CONFIRMED AND STRENGTHENED**

Metadata evidence:
https://app.bot.or.th/BTWS_STAT/statistics/DownloadFile.aspx?file=EC_EI_003_S3_ENG.PDF

It states:
- table code: EC_EI_003_S3;
- frequency: monthly;
- lag: 1 month;
- schedule: last business day of following month;
- revision policy: revision is made when updated data become available.

### Stronger empirical evidence found in R2

Official BOT Web Statistics snapshots show real value changes between publication states.

Earlier official snapshot:
- Last updated 31 Aug 2026
- JUL 2026: 171.55 p
- JUN 2026: 157.51 r
- MAY 2026: 160.18 r

Later official snapshot:
- Last updated 30 Sep 2026
- JUL 2026: 171.89 r
- JUN 2026: 157.61 r
- MAY 2026: 163.01 r

Therefore revision is not merely theoretical; values can change between retrieval vintages.

Implication:
The project must preserve retrieved vintages before normalization/forecasting.

---

## C11 — Revised/discontinued resources prove series lifecycle
**Round-1 wording:** revised/discontinued resources imply series/table identity is not permanently static and future metadata should support supersession.

**R2 status:** **CORRECTED / ROUND-1 OVERCLAIMED**

What official evidence actually proves:
- BOT publishes revised/replaced **statistical table / Report ID** mappings.
- BOT publishes discontinued **tables**.

Examples:
- revised-table page maps Previous Report ID/Name → New Report ID/Name;
- discontinued-table page lists table/report identifiers no longer published.

Official evidence:
https://www.bot.or.th/en/statistics/revised-table-list.html
https://www.bot.or.th/th/statistics/discontinue-table-list.html

What is **not yet proven**:
- whether API **series codes** have an identical supersession/discontinuation lifecycle;
- whether Report ID/table replacement maps one-to-one to API series replacement.

### Corrected conclusion

Use:
> Table/report lifecycle changes are confirmed. API series-code lifecycle remains UNKNOWN and must be researched separately.

Do **not** yet encode table replacement as proof of API-series replacement.

This is the most important correction from Round 2.

---

## C12 — BOT should be modeled as a provider with multiple API products
**R2 status:** **CONFIRMED**

Independent product catalogue evidence shows separate products including:
- Statistics;
- Interest Rates;
- Exchange Rates;
- Debt Securities Auction;
- Others.

Official catalogue:
https://portal.api.bot.or.th/portal/catalogue-products

Independent examples:
- Exchange Rates has separate base paths such as /Stat-ExchangeRate/v2.
- Interest Rates exposes multiple independent REST listen paths.

Implication:
A BOT integration architecture should not assume one global BOT API schema or rate limit.

Provider → Product remains a sound architecture hypothesis.

---

# DESIGN HYPOTHESES REVALIDATED

## H01 — BTWS should be the default manual cross-check for the first Statistics proof
**R2 status:** **SUPPORTED / NOT YET FULLY PROVEN**

Evidence supporting it:
- official observations visible;
- table metadata;
- last-updated time;
- revision markers;
- downloadable metadata.

Missing evidence:
- exact one-to-one mapping between selected API series code and selected BTWS row.

Therefore:
- keep the hypothesis;
- do not declare one-to-one mapping until Day 3/5.

---

## H02 — Expected machine path is discovery → exact series code → observations
**R2 status:** **STRONGLY SUPPORTED**

Evidence:
- search-series searches statistical series;
- observations explicitly filters using series code;
- Observations docs point to downloadable official Statistics API list.

This path is safe as a working architecture hypothesis for Statistics discovery/acquisition.

---

# NEW FINDINGS

## NF01 — Official downloadable Statistics API/series list exists
Found through the Observations documentation.

Potential use:
- bootstrap Source/Series Registry;
- compare discovered series against official inventory;
- detect additions/removals over time.

Status:
**NEW FINDING — URL/format still UNKNOWN**

Round 3 should locate and inspect it without assuming stability.

---

## NF02 — Actual PCI value revisions are directly observable across BOT publication snapshots
This strengthens the vintage requirement beyond policy documentation.

Status:
**NEW FINDING — CONFIRMED**

Potential future test:
Store two retrieval vintages and prove that July 2026 can preserve both:
- 171.55 as previously published provisional value;
- 171.89 as later revised value.

Do not implement this test in Day 1.

---

## NF03 — Product-level rate limits differ
Statistics currently shows 2,000 calls/hour, while Exchange Rates and Interest Rates product pages currently show 200 calls/hour.

Status:
**NEW FINDING — CONFIRMED AT PRODUCT PAGE LEVEL**

Implication:
Rate limiting should eventually be modeled per product/configuration, not as one BOT-wide constant.

Detailed behavior belongs to Day 2.

---

# CONTRADICTIONS / CORRECTIONS LOG

| ID | Round-1 statement | R2 result | Action |
|---|---|---|---|
| CR-01 | Revised/discontinued resources imply API series lifecycle | Too broad | Restrict evidence to table/report lifecycle; API-series lifecycle = UNKNOWN |
| CR-02 | BTWS as default API cross-check | Reasonable but not proven one-to-one | Keep as design hypothesis until selected API series is mapped |
| CR-03 | BOT rate can be treated at provider level | Not stated explicitly in R1, but R2 shows product rates differ | Future config must be product-aware |

No core contradiction was found for:
- new gateway;
- Statistics product;
- three Statistics API families;
- search-series discovery;
- observations by series code;
- BTWS official status;
- provider→product architecture.

---

# ROUND-2 CONFIDENCE MATRIX

| Claim area | Status |
|---|---|
| New portal/gateway | CONFIRMED |
| 17 Sep 2025 migration date | CONFIRMED |
| Statistics API family map | CONFIRMED |
| search-series discovery role | CONFIRMED |
| observations by series code | CONFIRMED |
| BTWS official verification surface | CONFIRMED |
| PCI revision policy | CONFIRMED |
| Actual PCI value revisions | CONFIRMED |
| Multiple BOT API products | CONFIRMED |
| Table/report lifecycle changes | CONFIRMED |
| API series-code lifecycle | STILL UNKNOWN |
| Exact BTWS row ↔ API series mapping | STILL UNKNOWN |
| Official API-list direct machine URL/format | STILL UNKNOWN |

---

# IMPACT ON DAY-1 FROZEN FINDINGS

Day 1 remains valid, but one statement must be narrowed:

### Replace
“Series/table identity is not permanently static.”

### With
“BOT statistical **table/report identities** are demonstrably revised/replaced/discontinued. Equivalent lifecycle behavior for API **series codes** is not yet proven.”

Architecture impact:
- support table/report lifecycle metadata when such objects are represented;
- do not invent API-series supersession relationships without direct evidence;
- keep Provider → Product;
- keep discovery → exact series → observations;
- model limits/config at product level.

---

# ROUND-2 RESULT

**Independent Revalidation: PASS**

Meaning:
- core ecosystem claims survived independent verification;
- one overclaim was found and corrected;
- three useful new findings were added;
- unresolved items remain explicit.

This is **not** Day 1 final freeze.

---

# NEXT ROUND

## Round 3 — Gap Hunt

Primary questions:
1. Where is the downloadable official **List of Statistics APIs** and what format/schema does it use?
2. Are there other current Statistics discovery/metadata surfaces missed in Round 1?
3. Does BOT expose table/report IDs inside API series metadata?
4. Is there an official mapping between BTWS Report ID/table rows and API series codes?
5. Are there archive/version surfaces for API specifications or statistical metadata?
6. What ecosystem component is still missing from the current map?

Round 3 should search for what R1/R2 **missed**, not re-prove already confirmed claims.

---

## Rule

Official source first.  
Independent evidence before agreement.  
UNKNOWN ≠ PASS.  
Do not advance to Day 2 while the user is explicitly deepening Day 1 rounds.
