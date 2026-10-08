# Issue #11 — Day 01 Round 4
## BOT Architecture Challenge

**Date:** 2026-10-08  
**Parent:** Day 01 — BOT Data Ecosystem Map  
**Round:** R4 — Architecture Challenge  
**Inputs:** R1 Discovery, R2 Independent Revalidation, R3 Gap Hunt  
**Status:** ARCHITECTURE HYPOTHESIS ONLY — no baseline schema migration in this round

---

# PURPOSE

Rounds 1–3 established that BOT exposes economic data through multiple parallel surfaces:

- API products;
- API series;
- sector/catalog pages;
- BTWS tables;
- downloadable files;
- metadata documents;
- revision/discontinuation pages;
- concept/index pages.

Round 4 challenges the earlier simplifying model:

`Provider → Product → Series → Observation`

Question:

> What is the smallest architecture that can represent BOT truthfully without forcing API series, BTWS tables, report IDs, downloadable files, and internal canonical series into the same identity?

---

# ARCHITECTURE TEST CRITERIA

A candidate architecture must satisfy all of these:

1. **No false identity**
   - `table_code`, `report_id`, and API `series_code` must never be treated as the same identifier unless evidence proves equivalence.

2. **Multiple access surfaces**
   - BOT API and BOT publication/file surfaces must both fit naturally.

3. **Canonical internal series**
   - Thailand Economic OS must retain its own stable `series_id` independent of provider-specific identifiers.

4. **Evidence-backed mapping**
   - cross-surface or source→canonical mappings must be explicit relationships with evidence.

5. **Lifecycle**
   - tables/reports may be revised, replaced, discontinued, or superseded.

6. **Version awareness**
   - API/product/spec versions must be recordable without redefining the provider.

7. **Minimality**
   - do not create a new entity for every page/button/document if a typed asset/relationship is sufficient.

8. **Cross-provider reuse**
   - the pattern should later support NESDC, TPSO, MOF, and Customs without being BOT-specific.

---

# OPTION A — KEEP THE SIMPLE HIERARCHY

```text
Provider
  ↓
Product
  ↓
Series
  ↓
Observation
```

## Strengths
- simple;
- easy to understand;
- works reasonably for pure APIs.

## Failures against BOT evidence

### A1 — BTWS table is not naturally an API Product
A publication table such as:
- table_code `EC_EI_003_S3`
- report_id `995`

is not the same kind of object as:
- Statistics API product;
- API `series_code`.

### A2 — one table may contain multiple conceptual rows/series
A BOT table can contain multiple indicators/components.

Therefore:
`Table ≠ Series`.

### A3 — API series ↔ table mapping is unproven
R3 found no authoritative one-to-one mapping.

Therefore forcing both into one `Series` identity would manufacture certainty.

### A4 — files and metadata become awkward
Excel/CSV/metadata PDF/spec exports are source artifacts, not series.

### Verdict
**REJECT as complete provider model.**

Keep the simple hierarchy only as a local view inside a specific API product, not as the entire BOT source architecture.

---

# OPTION B — TWO PARALLEL PROVIDER BRANCHES

```text
Provider: BOT
│
├── API / Machine Access
│   ├── Product
│   ├── API
│   └── Provider Series
│
└── Publication / Human-File Access
    ├── Domain / Catalog
    ├── Table / Report
    └── Artifact
```

Then map both branches to internal canonical economic series.

## Strengths
- matches observed BOT reality;
- preserves identifier namespaces;
- supports both API and table/file evidence;
- avoids false one-to-one assumptions.

## Weakness
If implemented literally with many tables/classes, it could become over-modeled.

### Verdict
**SUPPORTED, but should be implemented with a minimal generic entity vocabulary.**

---

# OPTION C — ONE GENERIC “SOURCE OBJECT” FOR EVERYTHING

```text
Provider
  ↓
SourceObject(type=product|api|series|table|file|metadata|...)
```

## Strengths
- very flexible;
- few database tables.

## Weaknesses
- weak semantic constraints;
- every query becomes type-dependent;
- easy to mix incompatible identities;
- loses clarity between a series and a file;
- harder to enforce contracts.

### Verdict
**REJECT as the primary conceptual model.**

A generic asset table may still be useful for files/documents, but not for all provider objects.

---

# RECOMMENDED MINIMAL MODEL — R4 HYPOTHESIS

The best balance is a **small typed provider graph** plus an independent canonical-series layer.

```text
                         ┌─────────────────────┐
                         │   Provider: BOT     │
                         └─────────┬───────────┘
                                   │
                ┌──────────────────┴───────────────────┐
                │                                      │
        MACHINE ACCESS                         PUBLICATION ACCESS
                │                                      │
        ┌───────▼────────┐                     ┌───────▼────────┐
        │ Source Product │                     │ Publication    │
        │ Statistics     │                     │ Domain/Catalog │
        └───────┬────────┘                     └───────┬────────┘
                │                                      │
        ┌───────▼────────┐                     ┌───────▼────────┐
        │ Source API     │                     │ Source Table   │
        │ observations   │                     │ EC_EI_003_S3   │
        └───────┬────────┘                     │ report_id 995  │
                │                              └───────┬────────┘
        ┌───────▼────────┐                             │
        │ ProviderSeries │                       ┌─────▼──────┐
        │ series_code X  │                       │ Artifacts  │
        └───────┬────────┘                       │ CSV/XLS/PDF│
                │                                └────────────┘
                │
                └──────────────┐
                               │ evidence-backed mapping
                               ▼
                    ┌─────────────────────┐
                    │ Canonical Series    │
                    │ BOT_PCI_TOTAL       │
                    └─────────┬───────────┘
                              │
                              ▼
                    Canonical Observations
```

Important:
A Source Table may also map to the same Canonical Series, but only when row/table semantics are proven.

---

# ENTITY HYPOTHESIS

## 1. Provider
Represents the publishing institution.

Example:
`BOT`

Fields conceptually:
- provider_id
- name
- official_domain
- last_verified

This remains close to current `Source`, but “Source” may be too broad if it is used for both institution and access channel.

---

## 2. Source Product
A provider-owned machine-access product or service grouping.

Examples:
- BOT Statistics
- BOT Exchange Rates
- BOT Interest Rates

Why it deserves identity:
- independent rate limits;
- independent API families;
- independent versions/plans/permissions.

---

## 3. Source API
A callable interface within a product.

Examples:
- categorylist
- search-series
- observations

Fields conceptually:
- api_name
- base/listen path
- spec_version
- method(s)
- current canonical URL
- legacy aliases
- last_verified
- spec checksum/reference

This avoids putting API version on the provider or product globally.

---

## 4. Provider Series
An external machine-readable statistical series identity issued by the provider.

Key:
- `provider_series_code`

Important:
This is **not** our internal `series_id`.

Example conceptual relationship:
`BOT API series code ??? → BOT_PCI_TOTAL`

The exact BOT code remains UNKNOWN until later research.

---

## 5. Publication Table
A provider-published human/file-oriented statistical table/report.

For BOT it can carry multiple namespaced identifiers:
- `table_code = EC_EI_003_S3`
- `report_id = 995`

Important:
Table ≠ API Series.

A table may contain:
- multiple rows;
- multiple concepts;
- multiple series-like values.

---

## 6. Source Artifact
A retrievable supporting object.

Types:
- CSV
- XLS/XLSX
- PDF metadata
- API spec export
- raw API response
- HTML snapshot

Fields conceptually:
- artifact_type
- canonical_url
- retrieved_at
- checksum
- content_type
- related source object
- version/date if known

This is where a generic typed-asset model is useful.

---

## 7. Canonical Series
This is the Thailand Economic OS economic-series identity already represented conceptually by the Data Contract.

Examples:
- `BOT_PCI_TOTAL`
- `BOT_CREDIT_HOUSEHOLD`

Properties:
- stable internal ID;
- economic meaning;
- frequency;
- unit;
- seasonal adjustment;
- description.

It must remain independent of provider-specific IDs.

---

## 8. Source Mapping
Explicit relationship connecting external provider objects to a canonical series.

Examples:

```text
ProviderSeries(API code X)
  → REPRESENTS
CanonicalSeries(BOT_PCI_TOTAL)

PublicationTable(EC_EI_003_S3)
  → CONTAINS
TableRow(PCI total?)      [only if row identity is modeled/proven]

TableRow / Table semantic target
  → VERIFIES / REPRESENTS
CanonicalSeries(BOT_PCI_TOTAL)
```

Minimum mapping fields conceptually:
- from_object
- to_object
- relation_type
- evidence_ref
- confidence
- valid_from
- valid_to
- last_verified

Mapping must be evidence-backed.

---

# IDENTIFIER NAMESPACE DECISION HYPOTHESIS

Identifiers must be namespaced.

Examples:

```text
BOT:table_code:EC_EI_003_S3
BOT:report_id:995
BOT:api_series:<UNKNOWN>
BOT:api_name:observations
BOT:product:statistics
```

Rules:
1. Same raw string in different namespaces is not the same identity.
2. Never promote a provider ID to canonical series ID.
3. Aliases preserve legacy URLs/names but do not redefine identity.
4. Supersession is a relationship, not an ID overwrite.

---

# ENTITY VS ATTRIBUTE VS RELATIONSHIP

## Entity
Use an entity when it has independent lifecycle/identity.

Recommended:
- Provider
- Source Product
- Source API
- Provider Series
- Publication Table
- Canonical Series
- Source Artifact

## Attribute
Use an attribute when it describes one entity but has no useful independent lifecycle.

Examples:
- API spec version on Source API
- table title on Publication Table
- MIME type on Artifact
- rate-limit documentation on Product/API config
- last_verified

## Relationship
Use a relationship when two independently valid objects are connected.

Examples:
- Provider HAS_PRODUCT Product
- Product EXPOSES_API API
- API EXPOSES_SERIES ProviderSeries
- PublicationDomain LISTS_TABLE Table
- Table HAS_ARTIFACT Artifact
- ProviderSeries REPRESENTS CanonicalSeries
- Table/row VERIFIES CanonicalSeries
- Table SUPERSEDES Table
- LegacyURL ALIAS_OF current endpoint

---

# SAME ECONOMIC CONCEPT CAN MAP TO MULTIPLE SOURCE OBJECTS

**Architecture answer: YES, explicitly allow it.**

Example conceptual model:

```text
Economic concept:
Private Consumption

          ┌─────────────── API series code
          │
Canonical Series BOT_PCI_TOTAL
          │
          ├─────────────── BTWS table/row
          │
          └─────────────── CSV/XLS publication artifact
```

The internal canonical series provides one stable semantic anchor.

External objects remain separate evidence/acquisition surfaces.

This is preferable to choosing one BOT representation as “the real identity.”

---

# RAW VS CANONICAL OBSERVATION DECISION

The current Data Contract defines canonical Observation.

R4 recommends distinguishing conceptually:

## Raw Source Record / Raw Artifact
What BOT actually returned/published at retrieval time.

## Canonical Observation
What Thailand Economic OS normalized into:
- canonical series;
- canonical period;
- value;
- unit;
- vintage;
- quality.

Trace:

```text
Provider object
  ↓
retrieval
  ↓
Raw Artifact / Raw Source Record
  ↓
parser
  ↓
mapping
  ↓
Canonical Series
  ↓
Canonical Observation
```

This does not require changing V0.1 Data Contract today; it clarifies the future ingestion boundary.

---

# DOES V0.1 ARCHITECTURE NEED TO CHANGE NOW?

**R4 decision: NO — not yet.**

Reason:
V0.1 architecture is intentionally high-level:
`PUBLIC DATA SOURCES → CONNECTORS → RAW VAULT → ...`

R4 findings refine the internal structure of “PUBLIC DATA SOURCES / CONNECTORS” but do not invalidate the high-level pipeline.

The V0.1 freeze rule says changes to core contracts require:
- Decision Log;
- version/schema change;
- migration;
- tests;
- review.

Therefore Round 4 should **not** silently modify:
- `docs/ARCHITECTURE.md`
- schemas
- production database design.

Instead, carry this R4 hypothesis into later Day-1 rounds and Issue #11 final source inventory.

---

# DOES V0.1 DATA CONTRACT NEED TO CHANGE NOW?

**R4 decision: NO — but one terminology risk is identified.**

Current contract:
- Source
- Series
- Observation

Potential ambiguity:
`Source` might be read as both:
- publishing institution;
- API/file/table source object.

R4 recommends that future V0.2/V0.3 design clarify naming, potentially:

```text
Provider
SourceObject / SourceAsset
ProviderSeries
CanonicalSeries
Observation
```

But no breaking change should occur before:
- other P0 providers are researched;
- we know whether the BOT pattern generalizes.

This prevents BOT-specific overfitting.

---

# CROSS-PROVIDER GENERALIZATION TEST

## NESDC
Likely:
- Provider
- publication/files
- tables/artifacts
- canonical series
No API Product may be required.

Model fits.

## TPSO
Likely:
- Provider
- API product/interface
- external codes
- canonical series
Model fits.

## MOF
Likely:
- Provider
- API/file interfaces
- fields/series
- canonical series
Model fits.

## Customs
Likely:
- Provider
- form/query interface
- CSV artifact
- dimensions/series-like selection
- canonical series
Model likely fits.

Conclusion:
Parallel access/publication surfaces appear more reusable than BOT-only hierarchy.

---

# ARCHITECTURE CHALLENGE MATRIX

| Question | R4 answer |
|---|---|
| Is Provider→Product→Series→Observation enough for all BOT? | NO |
| Is it still useful inside API products? | YES |
| Should BOT Table and API Series be separate identities? | YES |
| Should table_code/report_id/series_code share namespace? | NO |
| Should canonical series use provider ID directly? | NO |
| Can one canonical concept map to multiple source objects? | YES |
| Must mappings carry evidence? | YES |
| Do we need dozens of BOT-specific entity types? | NO |
| Should files/specs be typed Source Artifacts? | YES |
| Should V0.1 architecture be rewritten now? | NO |
| Should schema migration happen now? | NO |
| Should this hypothesis survive testing against other P0 sources first? | YES |

---

# R4 ARCHITECTURE HYPOTHESIS

Use:

```text
Provider
├── Machine Access
│   ├── Source Product
│   ├── Source API
│   └── Provider Series
│
└── Publication Access
    ├── Publication Domain/Catalog
    ├── Publication Table
    └── Source Artifact

Provider Series / Publication semantic target
        ↓ evidence-backed mapping
Canonical Series
        ↓
Canonical Observation
```

with namespaced external identifiers and immutable evidence-backed mappings.

---

# WHAT R4 REJECTS

1. One BOT-wide API object.
2. Table code = report ID = API series code.
3. Provider ID reused as canonical series ID.
4. Silent mapping by matching titles.
5. Treating downloadable files as “series.”
6. Adding dozens of BOT-specific database entities before testing other providers.
7. Editing V0.1 architecture/schema immediately from one-provider evidence.

---

# ROUND-4 RESULT

**Architecture Challenge: PASS**

Outcome:
- the simple model was challenged and found incomplete;
- a minimal parallel-surface architecture is supported;
- canonical internal series remains separate from provider identifiers;
- no baseline schema/architecture migration is authorized yet;
- hypothesis must be tested against source-role and cross-provider evidence before becoming a formal Decision Log entry.

---

# NEXT ROUND

## Round 5 — Source Relationship Mapping

Goal:
Assign explicit roles to every BOT surface and relationship discovered so far.

Questions:
1. Which surfaces are authoritative for acquisition?
2. Which are authoritative for metadata?
3. Which are verification-only?
4. Which are lifecycle/change signals?
5. Which objects can substitute for another during failure?
6. Which relationships are confirmed vs hypothetical?
7. What is the minimum relationship graph an agent needs to recover BOT context correctly?

Expected output:
A Source-Role Matrix and relationship graph.

Do not implement database tables.

---

## Rule

Model only identities and relationships supported by evidence.  
Prefer explicit UNKNOWN over invented equivalence.  
Do not rewrite frozen architecture until the research hypothesis generalizes beyond BOT.
