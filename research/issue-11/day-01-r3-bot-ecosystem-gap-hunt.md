# Issue #11 — Day 01 Round 3
## BOT Ecosystem Gap Hunt

**Date:** 2026-10-08  
**Parent:** Day 01 — BOT Data Ecosystem Map  
**Round:** R3 — Gap Hunt  
**Method:** Search for ecosystem components, identifiers, discovery surfaces, download paths, and maintenance/versioning signals that R1/R2 did not fully map.  
**Rule:** Do not re-prove already confirmed claims unless needed to identify a gap.

---

## ROUND-3 PURPOSE

Round 1 discovered the ecosystem.  
Round 2 independently revalidated the claims.  
Round 3 asks:

> What important BOT data surface, identifier, lifecycle signal, mapping, archive, or documentation behavior is still missing from our current map?

Primary targets:
1. locate the official downloadable **List of Statistics APIs**;
2. inspect possible mapping between BTWS table/report identifiers and API series codes;
3. look for archive/version surfaces;
4. find any metadata/download/discovery surfaces missed in R1/R2;
5. identify navigation or documentation inconsistencies that could mislead automation.

---

# GAP FINDINGS

## G01 — Official downloadable “List of Statistics APIs” definitely exists
**Status:** CONFIRMED EXISTENCE / DIRECT FILE LOCATION STILL UNKNOWN

Official Observations documentation explicitly says users can download series codes from a **List of Statistics APIs** and shows a “Download API list Document” action.

Official evidence:
https://portal.api.bot.or.th/portal/catalogue-products/statistics-1/e2dcfd41460e49a86276db01aeb3cd1f/docs

What is now confirmed:
- the list is an official BOT artifact;
- it is intended as an authoritative series-code inventory for Statistics API users;
- it may be more suitable than free-text search alone for bootstrapping a registry.

What remains UNKNOWN:
- direct/stable download URL;
- file type;
- schema/columns;
- whether it includes table/report identifiers;
- whether it changes in place or is versioned;
- whether historical copies are retained.

**Design impact:** this file should be treated as a high-priority registry-bootstrap candidate, but must not be assumed stable until inspected directly.

---

## G02 — Public sector pages form a separate table-catalog layer
**Status:** NEW FINDING — CONFIRMED

R1/R2 emphasized:
- API portal;
- BTWS table page;
- BTWS metadata.

R3 found a distinct official **sector index/catalog layer** on bot.or.th.

Examples:
- Real Sector:
  https://www.bot.or.th/en/statistics/real-sector.html
- Monetary Statistics:
  https://www.bot.or.th/en/statistics/monetary-statistic.html

These pages expose report catalogs with columns such as:
- Report ID / table code;
- Report Name;
- Excel file;
- CSV file;
- Metadata;
- Last Updated.

This is not just navigation. It is a structured publication catalog that may serve as:
- table discovery;
- file-download discovery;
- last-update monitoring;
- metadata discovery;
- table lifecycle observation.

### Updated table-side ecosystem

```text
BOT Statistics domain page
        ↓
sector catalog
        ↓
table code / report entry
        ├── Excel
        ├── CSV
        ├── Metadata
        └── BTWS table
```

**Design impact:** BOT's human/file ecosystem is richer than “BTWS page only.” Future source inventory should distinguish:
- sector catalog;
- BTWS report;
- downloadable file;
- metadata document.

---

## G03 — Table code and BTWS Report ID are distinct identifiers
**Status:** NEW FINDING — CONFIRMED

Example:
- table code: `EC_EI_003_S3`
- BTWS URL reportID: `995`
- title: Private Consumption Index and Components (Seasonally Adjusted)

Official table:
https://app.bot.or.th/BTWS_STAT/statistics/BOTWEBSTAT.aspx?language=ENG&reportID=995

Official metadata:
https://app.bot.or.th/BTWS_STAT/statistics/DownloadFile.aspx?file=EC_EI_003_S3_ENG.PDF

Therefore BOT table-side identity already includes at least two distinct keys:
1. **table_code**
2. **report_id**

They must not be conflated.

**Still UNKNOWN:** whether either maps directly to an API series code.

### Design impact

Potential future metadata model:

```text
BOT Table
├── table_code
├── report_id
├── title
├── sector/domain
├── files
└── metadata

BOT API Series
└── series_code

Table ↔ API Series mapping
= explicit relationship only when proven
```

---

## G04 — No authoritative BTWS table/report ↔ API series mapping was found in R3
**Status:** STILL UNKNOWN

Searches using:
- table code `EC_EI_003_S3`;
- reportID `995`;
- Private Consumption Index;
- “series code”;
- current Statistics documentation

did not surface an official mapping from:
- BTWS table code/report ID
to
- Statistics API series code.

This is an important negative finding.

### What we must NOT do
Do not infer an API series code from:
- table code;
- reportID;
- row position;
- title text.

### Next likely bridge
The official downloadable **List of Statistics APIs** may contain the missing mapping or enough metadata to construct one.

This remains a Round-3 unresolved gap and a later R4/R5 input.

---

## G05 — Current BOT website contains a stale link to the legacy API portal
**Status:** NEW FINDING — CONFIRMED

The current BOT Statistics page includes a BOT API navigation link pointing to:
`https://apiportal.bot.or.th/bot/public`

Following that link currently fails.

At the same time, BOT's current API portal explicitly states the new system is:
- Developer Portal: https://portal.api.bot.or.th/
- Gateway: https://gateway.api.bot.or.th/
- in use since 17 Sep 2025.

Official current system:
https://portal.api.bot.or.th/

### Gap interpretation
Official BOT web content itself can contain stale navigation after an API migration.

### Design impact
“Official domain” alone is insufficient as a freshness signal.

Future automation should record:
- canonical current URL;
- observed redirect/failure;
- evidence date;
- legacy/current classification.

A canonical-link registry is justified.

---

## G06 — API specifications are versioned per API, not just per product
**Status:** NEW FINDING — CONFIRMED

Current Statistics documentation shows different API spec versions:
- Stat Category: **v1.0.0**
- Search Stat APIs: **v1.0.0**
- Observations: **v1.0.3**

Current portal documentation also exposes an **Export** function on API documentation pages.

Other products similarly expose explicit API versions (for example Exchange Rates v2.0.2).

### What R3 did NOT find
- a public changelog for Statistics APIs;
- an archive of prior Statistics specs;
- a documented compatibility policy.

### Design impact
Future retrieval/connector metadata should preserve:
- product;
- API name;
- API/spec version observed;
- retrieval date;
- possibly exported OpenAPI/spec checksum.

Do not model “BOT Statistics v1” as one single version field.

---

## G07 — A public spec-export surface exists, but historical spec archive is not evident
**Status:** PARTIALLY CONFIRMED

Current portal pages show:
- API documentation;
- explicit version numbers;
- Export / DOWNLOAD SPEC actions on products/APIs.

This is enough to justify preserving a local copy/checksum of the API specification when implementation begins.

What remains UNKNOWN:
- export format for Statistics;
- stable export URL;
- whether old spec revisions remain retrievable after updates.

### Design impact
V0.2 connector implementation should eventually snapshot the relevant spec artifact in evidence, not depend only on live documentation.

---

## G08 — “Open Data” on BOT website is a false friend for this project
**Status:** NEW FINDING — CONFIRMED

BOT has an official “Open Data” page, but it concerns consumer/business rights to share financial-service-provider data between providers.

It is **not** the statistical open-data publication surface used by Thailand Economic OS.

Official page:
https://www.bot.or.th/en/financial-innovation/digital-finance/open-data.html

### Design impact
Search/agent workflows must distinguish:
- BOT statistical/public economic data;
- BOT “Open Data” consumer data-sharing initiative.

Keyword-based discovery alone could route an agent to the wrong subsystem.

---

## G09 — BOT curates macro-indicator concept → BTWS table links
**Status:** NEW FINDING — CONFIRMED

The “Economic and Financial Index and Indicators” page provides a curated macro layer linking concepts such as:
- exports;
- imports;
- trade balance;
- current account;
- reserves;
- public debt;
- money;
- household loans;
- interest rates;
- exchange rates

to specific BTWS tables.

Official page:
https://www.bot.or.th/en/statistics/economic-and-financial-index-and-indicators.html

### Why this matters
This page is a semantic bridge:

```text
economic concept
    ↓
official BOT table
    ↓
BTWS report
```

It does **not** prove API-series mapping, but it is useful for:
- selecting high-value proof datasets;
- validating conceptual coverage;
- linking economic-state dimensions to official table families later.

---

# UPDATED BOT ECOSYSTEM MAP AFTER R3

```text
BANK OF THAILAND
│
├── BOT Statistics / Dissemination
│   │
│   ├── Statistics domain landing
│   │
│   ├── Sector catalog pages
│   │   ├── table_code
│   │   ├── report name
│   │   ├── Excel
│   │   ├── CSV
│   │   ├── Metadata
│   │   └── Last Updated
│   │
│   ├── Economic & Financial Indicator page
│   │   └── concept → BTWS table bridge
│   │
│   ├── Revised/discontinued table resources
│   │
│   └── BTWS
│       ├── report_id
│       ├── table_code
│       ├── observations
│       ├── Download
│       ├── Metadata PDF
│       └── p/r markers
│
├── BOT Developer Portal
│   │
│   ├── Product Catalogue
│   │
│   ├── Statistics Product
│   │   ├── categorylist v1.0.0
│   │   ├── search-series v1.0.0
│   │   ├── observations v1.0.3
│   │   ├── API spec export surface
│   │   └── downloadable List of Statistics APIs
│   │       └── direct file/schema still UNKNOWN
│   │
│   ├── Exchange Rates
│   ├── Interest Rates
│   ├── Debt Securities Auction
│   └── other products
│
├── Migration / Operations
│   ├── migration guide
│   ├── maintenance notices
│   └── dashboard/performance analytics
│
└── Separate initiative: “Open Data”
    └── consumer data-sharing regime
        (NOT the statistical-data surface)
```

---

# GAP MATRIX

| Gap | Status after R3 | Next action |
|---|---|---|
| Direct URL of List of Statistics APIs | UNKNOWN | locate/inspect exported file |
| File format/schema of API list | UNKNOWN | inspect actual download |
| BTWS table_code ↔ API series_code mapping | UNKNOWN | use API list/search-series later |
| report_id ↔ series_code mapping | UNKNOWN | do not infer |
| Statistics spec history/changelog | UNKNOWN | search portal/help/contact if needed |
| Stable spec-export URL | UNKNOWN | inspect export action during implementation/research |
| Table catalog layer | FOUND | add to architecture |
| Concept → BTWS table bridge | FOUND | use for dataset selection |
| Stale official API link | FOUND | add canonical URL/freshness rule |
| “Open Data” false friend | FOUND | exclude from statistical source map |

---

# ROUND-3 DESIGN IMPACT

## 1. Add a table-publication layer
Provider → Product → Series is insufficient to describe BOT's complete publication ecosystem.

For source metadata, we likely need:

```text
Provider
├── API Product
│   └── API Series
└── Publication Domain
    └── Table/Report
        └── File/Metadata
```

Do not force BTWS tables into the API Product model.

## 2. Maintain explicit identifier namespaces
At minimum:
- BOT table_code
- BOT BTWS report_id
- BOT API series_code

Namespace must be part of identity.

## 3. Canonical URL/freshness rule
Because current official pages can still contain legacy links:
- canonical URL must be verified;
- last_verified must be recorded;
- legacy URLs should be preserved as aliases, not used as current endpoints.

## 4. Snapshot API specs
Per-API versions differ. Connector evidence should preserve the observed specification version/checksum.

## 5. Do not assume cross-surface mappings
Any table ↔ API-series relationship must be evidence-backed.

---

# ROUND-3 RESULT

**Gap Hunt: PASS**

Meaning:
- multiple previously unmapped ecosystem components were found;
- one important navigation inconsistency was found;
- identifier namespaces were clarified;
- direct API-list location/mapping questions remain UNKNOWN and are explicitly isolated.

This does **not** mean Day 1 is frozen.

---

# NEXT ROUND

## Round 4 — Architecture Challenge

Challenge the updated architecture itself.

Questions:
1. Is `Provider → Product → Series → Observation` still sufficient anywhere, or must we explicitly model parallel publication/table/file surfaces?
2. Should BOT Table and BOT API Series be separate entities?
3. What should be an entity vs an alias vs a relationship?
4. Where do table_code, report_id, series_code, API name, product name, and spec version belong?
5. Can the same economic concept map to multiple BOT publication/API objects?
6. What minimal architecture prevents later redesign without over-modeling?

Round 4 must produce an architecture decision hypothesis, not implementation.

---

## Rule

Find missing structure before building structure.  
Official source first.  
UNKNOWN ≠ PASS.  
Do not advance to Day 2 while Day 1 rounds are intentionally active.
