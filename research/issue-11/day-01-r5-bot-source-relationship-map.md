# Issue #11 — Day 01 Round 5
## BOT Source Relationship Mapping

**Date:** 2026-10-08  
**Parent:** Day 01 — BOT Data Ecosystem Map  
**Round:** R5 — Source Relationship Mapping  
**Inputs:** R1 Discovery, R2 Revalidation, R3 Gap Hunt, R4 Architecture Challenge  
**Status:** RELATIONSHIP HYPOTHESIS — no database/schema implementation in this round

---

# PURPOSE

R4 established that BOT cannot be represented faithfully as one chain of:

`Provider → Product → Series → Observation`

because BOT exposes multiple parallel official surfaces.

R5 assigns explicit roles to those surfaces so a future human or agent knows:

- where to acquire values;
- where to discover identifiers;
- where to read semantics;
- where to verify published values;
- where to detect lifecycle changes;
- where to detect operational outages/migrations;
- what may become a fallback;
- what must never be treated as equivalent without evidence.

The goal is a **source-role matrix + evidence-backed relationship graph**, not database tables.

---

# ROLE VOCABULARY

R5 uses the following role labels.

- **MACHINE_ACQUISITION_PRIMARY** — preferred machine path for official values.
- **DISCOVERY** — find products, APIs, series, tables, or identifiers.
- **API_CONTRACT** — authoritative API/interface specification.
- **SEMANTIC_METADATA** — unit/frequency/definition/revision-policy meaning.
- **HUMAN_VERIFICATION** — official human-readable cross-check surface.
- **PUBLICATION_CATALOG** — official table/file index.
- **PUBLICATION_ARTIFACT** — official CSV/XLS/PDF/etc.
- **LIFECYCLE_SIGNAL** — replacement/discontinuation/revision structure.
- **SEMANTIC_BRIDGE** — concept → official publication/table relationship.
- **AUTH_ADMIN** — credentials/subscription/application administration.
- **OPERATIONAL_TELEMETRY** — request/error/performance evidence.
- **AVAILABILITY_SIGNAL** — maintenance/outage information.
- **MIGRATION_AUTHORITY** — current vs legacy interface mapping.
- **FALLBACK_CANDIDATE** — may be used if equivalence/stability is later proven.
- **LEGACY_ALIAS** — historical URL/interface retained for lineage only.
- **EXCLUDED_LOOKALIKE** — official BOT content not part of the statistical-data ecosystem.

---

# SOURCE-ROLE MATRIX

| BOT surface | Primary role | Secondary role | Authority scope | Automated acquisition status |
|---|---|---|---|---|
| Developer Portal root | DISCOVERY | AUTH_ADMIN | Current API ecosystem entry point | Navigation/admin only |
| Product Catalogue | DISCOVERY | API_CONTRACT | Current API products and product-level configuration | No observation acquisition |
| Statistics Product page | API_CONTRACT | DISCOVERY | Statistics product APIs, plan/rate info | No observation acquisition |
| API docs: categorylist | API_CONTRACT | DISCOVERY | Category/series browse contract | Discovery only |
| API docs: search-series | API_CONTRACT | DISCOVERY | Series search contract | Discovery only |
| API: observations | MACHINE_ACQUISITION_PRIMARY | API_CONTRACT | Machine-access statistical observations by series code | **Primary candidate** |
| List of Statistics APIs | DISCOVERY | REGISTRY_BOOTSTRAP candidate | Official series-code inventory | UNKNOWN until file inspected |
| BOT API Manual | AUTH_ADMIN | OPERATIONAL_TELEMETRY guidance | Subscription/application/token/dashboard workflow | Admin/ops only |
| Migration Guide | MIGRATION_AUTHORITY | LIFECYCLE_SIGNAL | Legacy→current gateway/auth changes | No data acquisition |
| Maintenance notices | AVAILABILITY_SIGNAL | OPERATIONAL_TELEMETRY | Planned API unavailability | No data acquisition |
| BOT Statistics landing | PUBLICATION_CATALOG | governance/schedule | Official statistics domains and release guidance | Navigation only |
| Sector catalog pages | PUBLICATION_CATALOG | DISCOVERY | Table code/name, files, metadata, last-updated | File discovery |
| BTWS table/report | HUMAN_VERIFICATION | publication surface | Official displayed values, report/table context, p/r markers | **Not primary machine path** |
| BTWS metadata PDF | SEMANTIC_METADATA | HUMAN_VERIFICATION | Definition, unit/base, frequency, lag, revision policy | Metadata only |
| Excel/CSV linked from catalog | PUBLICATION_ARTIFACT | FALLBACK_CANDIDATE | Official published file payload | Candidate; equivalence/stability must be proven |
| Revised table list | LIFECYCLE_SIGNAL | PUBLICATION_CATALOG | Table/report replacement lifecycle | No observation acquisition |
| Discontinued table list | LIFECYCLE_SIGNAL | PUBLICATION_CATALOG | Table/report discontinuation | No observation acquisition |
| Economic & Financial Indicators page | SEMANTIC_BRIDGE | DISCOVERY | Economic concept → BOT publication/table | Selection/navigation |
| “Open Data” financial data-sharing page | EXCLUDED_LOOKALIKE | none | Consumer/business data-sharing initiative | Exclude from statistics pipeline |

---

# AUTHORITY BY QUESTION

A future agent must not ask “Which BOT page is the source of truth?” without naming the question.

Different questions have different authoritative surfaces.

## Q1 — “How do I retrieve statistical observations by API?”
Authority order:

1. current **Statistics API documentation**
2. current **observations endpoint**
3. migration guide for current/legacy distinction

BTWS does not define the API contract.

---

## Q2 — “What is the official series identifier?”
Authority order:

1. official Statistics discovery interfaces:
   - search-series;
   - categorylist/series list;
   - official List of Statistics APIs when inspected.
2. persist exact provider series code with evidence.

Never derive API series code from:
- BTWS report ID;
- table code;
- title matching.

---

## Q3 — “What does the indicator mean?”
Authority order:

1. official table/API metadata specific to that indicator;
2. BTWS metadata PDF / official metadata source;
3. relevant official publication description.

A numerical API payload alone is insufficient semantic evidence.

---

## Q4 — “What value did BOT publicly show?”
Authority depends on target surface/vintage:

- API observation for machine/API publication state;
- BTWS/table/file for human/publication surface;
- raw retained artifact for what **our system observed at retrieval time**.

If values differ, do not silently choose one.

Investigate:
- retrieval time;
- publication/update time;
- provisional/revised state;
- source surface;
- exact semantic mapping.

---

## Q5 — “Was a table replaced or discontinued?”
Authority:

1. Revised Table List;
2. Discontinued Table List;
3. relevant table/catalog evidence.

This is confirmed for table/report lifecycle.

It does **not** automatically establish API series-code lifecycle.

---

## Q6 — “Which API endpoint/header is current?”
Authority:

1. current Developer Portal/API docs;
2. Migration Guide for old→new mapping.

Legacy official URLs may remain visible elsewhere and must not override the canonical current interface.

---

## Q7 — “Is BOT API temporarily unavailable?”
Authority:

1. official maintenance notice / operational notice;
2. observed connector HTTP/network evidence;
3. application performance telemetry when accessible.

Do not classify maintenance as an authentication failure.

---

# RELATIONSHIP GRAPH

```text
Provider(BOT)
│
├── HAS_PRODUCT
│   └── SourceProduct(Statistics)
│       │
│       ├── EXPOSES_API
│       │   ├── SourceAPI(categorylist)
│       │   │   └── DISCOVERS → ProviderSeries
│       │   │
│       │   ├── SourceAPI(search-series)
│       │   │   └── DISCOVERS → ProviderSeries
│       │   │
│       │   └── SourceAPI(observations)
│       │       └── RETURNS → Raw Observation Payload
│       │
│       └── HAS_REGISTRY_ARTIFACT
│           └── List of Statistics APIs
│               └── location/schema = UNKNOWN
│
├── PUBLISHES_DOMAIN
│   └── Statistics Domain
│       │
│       ├── HAS_CATALOG
│       │   └── Sector Catalog
│       │       └── LISTS_TABLE → PublicationTable
│       │
│       ├── HAS_SEMANTIC_BRIDGE
│       │   └── Economic/Financial Indicator page
│       │       └── LINKS_CONCEPT_TO → PublicationTable
│       │
│       └── HAS_LIFECYCLE_SIGNAL
│           ├── Revised Table List
│           └── Discontinued Table List
│
└── PublicationTable
    ├── HAS_NAMESPACE_ID → table_code
    ├── HAS_NAMESPACE_ID → report_id
    ├── RENDERS_AS → BTWS
    └── HAS_ARTIFACT
        ├── CSV
        ├── XLS/XLSX
        └── Metadata PDF
```

Then, only with evidence:

```text
ProviderSeries
    │
    └── REPRESENTS ──────┐
                         ▼
                  CanonicalSeries
                         ▲
                         │
Publication semantic target / table row
    └── VERIFIES or REPRESENTS
       [only if mapping is proven]
```

---

# CONFIRMED RELATIONSHIPS

## R01 — BOT HAS_PRODUCT Statistics
**Status:** CONFIRMED

Evidence:
current Developer Portal product catalogue and Statistics product.

---

## R02 — Statistics EXPOSES_API categorylist/search-series/observations
**Status:** CONFIRMED

---

## R03 — search-series DISCOVERS ProviderSeries
**Status:** CONFIRMED at contract level

Exact response fields remain later research.

---

## R04 — observations USES/RETURNS observations for a ProviderSeries code
**Status:** CONFIRMED at contract level

Exact live schema remains Day 4.

---

## R05 — BOT statistics sector catalog LISTS PublicationTable entries
**Status:** CONFIRMED

Catalog entries expose table/report names plus file/metadata/update information.

---

## R06 — PublicationTable RENDERS_AS BTWS table/report
**Status:** CONFIRMED for inspected examples

Example:
- `table_code = EC_EI_003_S3`
- `report_id = 995`

These identifiers remain distinct.

---

## R07 — PublicationTable HAS_ARTIFACT metadata/file resources
**Status:** CONFIRMED

Official catalogs/tables expose metadata and downloadable publication artifacts.

---

## R08 — Revised/Discontinued pages DESCRIBE table/report lifecycle
**Status:** CONFIRMED

They do not yet prove API-series lifecycle.

---

## R09 — Economic & Financial Indicator page LINKS economic concept → official table
**Status:** CONFIRMED

This is a semantic discovery relationship, not a series-code mapping.

---

## R10 — Migration Guide MAPS legacy interface → current interface
**Status:** CONFIRMED

This relationship should be retained for lineage/diagnostics.

---

# UNPROVEN RELATIONSHIPS

## U01 — PublicationTable REPRESENTS one ProviderSeries
**Status:** UNKNOWN / likely false as a general rule

Reason:
one table may contain multiple rows/components.

---

## U02 — table_code MAPS_TO API series_code
**Status:** UNKNOWN

No authoritative mapping found.

---

## U03 — report_id MAPS_TO API series_code
**Status:** UNKNOWN

No authoritative mapping found.

---

## U04 — API ProviderSeries and BTWS row are semantically identical for PCI total
**Status:** UNKNOWN until exact API series is discovered and values/metadata are compared.

---

## U05 — CSV/XLS can automatically replace Observations API during API outage
**Status:** NOT AUTHORIZED

Why:
before fallback, we must prove:
- semantic equivalence;
- frequency/unit identity;
- publication timing;
- revision behavior;
- machine-stable format.

Therefore official file ≠ automatic fallback by default.

---

# FALLBACK POLICY HYPOTHESIS

## Discovery fallback
Potential order:

```text
search-series
→ categorylist/series list
→ official List of Statistics APIs
```

But the API-list file must be inspected first.

---

## Observation acquisition fallback
Current status:

```text
observations API
→ PRIMARY

CSV/XLS official publication
→ FALLBACK_CANDIDATE only

BTWS HTML
→ HUMAN VERIFICATION, not approved automated fallback
```

No automated fallback is authorized in R5.

---

## Metadata fallback
Potential order:

```text
indicator-specific official metadata
→ table metadata PDF
→ catalog/table publication description
→ UNKNOWN
```

Never manufacture missing semantic metadata from values alone.

---

# CONFLICT RESOLUTION POLICY

If two official BOT surfaces disagree:

## Do not
- overwrite one with the other;
- assume API is newer;
- assume BTWS is newer;
- average values;
- select the value matching expectation.

## Do
record:
- source surface;
- external identifier;
- retrieval time;
- source last-updated/release information;
- provisional/revised marker;
- raw checksum;
- semantic mapping confidence.

Then classify:

```text
SAME_SEMANTICS_DIFFERENT_VINTAGE
SEMANTIC_MAPPING_UNCERTAIN
PUBLICATION_LAG
SOURCE_SURFACE_MISMATCH
UNKNOWN_CONFLICT
```

The conflict itself becomes evidence.

---

# AGENT RECOVERY GRAPH — MINIMUM BOT CONTEXT

A future agent returning to BOT should need only this conceptual path:

```text
BOT Provider
│
├─ Machine values?
│   → Statistics Product
│   → discover exact ProviderSeries
│   → observations
│   → retain raw payload
│
├─ Meaning/unit/revision policy?
│   → official metadata
│   → BTWS metadata/table catalog
│
├─ Human cross-check?
│   → BTWS table/report
│
├─ File publication/fallback candidate?
│   → sector catalog
│   → CSV/XLS
│
├─ Table replaced/discontinued?
│   → lifecycle lists
│
├─ API migrated?
│   → migration guide
│
├─ API down?
│   → maintenance/ops evidence
│
└─ Need internal economic identity?
    → evidence-backed mapping
    → Thailand Economic OS CanonicalSeries
```

---

# SOURCE ROLE PRINCIPLES

## Principle 1 — Authority is question-specific
There is no single BOT surface that is best for:
- acquisition;
- metadata;
- lifecycle;
- verification;
- operational status.

## Principle 2 — Official does not mean interchangeable
API, BTWS, CSV, XLS, metadata, and lifecycle pages are all official but serve different roles.

## Principle 3 — Verification source is not automatically fallback source
BTWS may verify an API observation without being an approved automated acquisition fallback.

## Principle 4 — Mappings require proof
Cross-surface title similarity is not enough.

## Principle 5 — Preserve disagreement
Official-source discrepancies must be recorded as version/source evidence rather than “cleaned” silently.

---

# SOURCE-ROLE MATRIX FOR PCI EXAMPLE

Current known PCI publication objects:

```text
Concept: Private Consumption
│
├── Semantic bridge
│   └── BOT economic-indicator/publication navigation
│
├── Publication table
│   ├── table_code: EC_EI_003_S3
│   ├── report_id: 995
│   ├── BTWS values
│   └── metadata PDF
│
└── Statistics API series
    └── exact series_code: UNKNOWN
```

Current authority use:

| Need | Use |
|---|---|
| exact API series code | search-series / official API list |
| machine observation | observations API |
| human published cross-check | BTWS report 995 |
| table semantic metadata | EC_EI_003_S3 metadata |
| revision evidence | BTWS p/r + metadata + retained vintages |
| canonical internal identity | future `BOT_PCI_TOTAL` mapping after proof |

---

# ROUND-5 RESULT

**Source Relationship Mapping: PASS**

R5 produced:
- a role vocabulary;
- a source-role matrix;
- a relationship graph;
- authority-by-question rules;
- confirmed and unproven relationship sets;
- fallback policy hypothesis;
- conflict-resolution policy;
- minimum recovery graph for future agents.

No database tables were implemented.

---

# NEXT ROUND

## Round 6 — Evidence Hardening

Goal:
Turn important Day-1 conclusions into a compact claim/evidence register.

For each critical claim record:
- claim ID;
- exact statement;
- evidence URL/artifact;
- evidence date;
- authority scope;
- confidence;
- contradiction/caveat;
- last verified;
- what would invalidate it.

Priority claims:
1. current portal/gateway;
2. Statistics API family;
3. search-series role;
4. observations role;
5. table_code vs report_id distinction;
6. table lifecycle vs API-series lifecycle distinction;
7. product-level rate configuration;
8. publication catalog role;
9. metadata authority;
10. API/publication mapping remains UNKNOWN.

Expected output:
A hardened evidence register that Round 7 can use for contradiction resolution.

---

## Rule

Use the right source for the right question.  
Official ≠ interchangeable.  
Verification ≠ fallback.  
UNKNOWN ≠ PASS.
