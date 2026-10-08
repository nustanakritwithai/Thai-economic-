# BOT Day 01 — Ecosystem Map FROZEN v1.1

**Project:** Thailand Economic OS  
**Release:** V0.2 Core Data Connectors  
**Issue:** #11 — Inventory official P0 data endpoints  
**Research Day:** 1  
**Freeze date:** 2026-10-08  
**Status:** DAY 1 FROZEN v1.1 — GATE PASS; closure self-audit PASS 10/10  
**Not equivalent to:** BOT connector complete / Issue #11 complete / V0.2 complete

**Predecessor:** `day-01-bot-ecosystem-FROZEN-v1.md` is preserved unchanged as the pre-audit freeze.  
**Post-freeze hardening:** v1.1 fixes state/pointer/audit-hardening defects only; it does not add Day-2 research.

---

# 0. PROVENANCE / AUDIT INDEX

Primary supporting artifacts:
- R6 human evidence register: `research/issue-11/day-01-r6-bot-evidence-register.md`
- R6 machine evidence register: `research/issue-11/day-01-r6-bot-evidence-register.json`
- R7 contradiction resolution: `research/issue-11/day-01-r7-bot-contradiction-resolution.md`
- R7 machine contradiction register: `research/issue-11/day-01-r7-bot-contradictions.json`
- Day-1 closure self-audit: `research/issue-11/day-01-closure-audit.md`
- Day-1 gate: `research/issue-11/day-01-gate.md`
- Post-freeze limitations review: `research/issue-11/day-01-limitations-review.md`
- Machine-readable official evidence manifest: `research/issue-11/day-01-official-evidence-manifest.json`

Core official BOT evidence surfaces used during Day 1:
- https://portal.api.bot.or.th/
- https://portal.api.bot.or.th/migration
- https://portal.api.bot.or.th/manual
- https://portal.api.bot.or.th/portal/catalogue-products/statistics-1
- https://www.bot.or.th/en/statistics.html
- https://www.bot.or.th/en/statistics/revised-table-list.html
- https://app.bot.or.th/BTWS_STAT/statistics/BOTWEBSTAT.aspx?language=ENG&reportID=995

**Audit limitation:** Closure Audit is a same-agent recovery self-audit. It demonstrates that one file is sufficient for context recovery; it is not independent semantic certification. CI validates repository structure/consistency, not the truth of external BOT content.

**Evidence-preservation limitation:** Day-1 official evidence is URL/date/claim based. Immutable raw source snapshots/checksums of external web content are not yet a Day-1 guarantee.

---

# 1. DAY-1 PURPOSE

Day 1 answers:

> What is the current BOT data ecosystem, which official surfaces exist, what role does each surface play, how should their identifiers/relationships be modeled, and what must remain UNKNOWN before later BOT research days?

Day 1 does **not** finalize:
- live auth/error behavior;
- exact PCI API series code;
- live observations response schema;
- API revision metadata behavior;
- API↔BTWS exact mapping;
- rate-limit enforcement mechanics;
- automated file fallback.

Those belong to Day 2–6 or later evidence.

---

# 2. EXECUTIVE ECOSYSTEM MAP

```text
BANK OF THAILAND
│
├── MACHINE / API ACCESS
│   │
│   ├── Developer Portal
│   │   ├── Product Catalogue
│   │   ├── Subscription / Application / Token admin
│   │   └── Performance / error telemetry
│   │
│   └── Statistics Product
│       ├── categorylist
│       │   └── category / series browsing
│       ├── search-series
│       │   └── keyword/name/code → ProviderSeries candidates
│       ├── observations
│       │   └── ProviderSeries code → observation payload
│       └── List of Statistics APIs
│           └── official inventory exists; direct file mechanics UNKNOWN
│
├── PUBLICATION / HUMAN-FILE ACCESS
│   │
│   ├── Statistics landing
│   ├── Sector catalog pages
│   │   ├── table_code
│   │   ├── report/table title
│   │   ├── Excel
│   │   ├── CSV
│   │   ├── Metadata
│   │   └── Last Updated
│   │
│   ├── BTWS
│   │   ├── report_id
│   │   ├── table_code context
│   │   ├── published observations
│   │   ├── Download
│   │   ├── Metadata
│   │   └── p/r markers
│   │
│   └── Metadata documents
│       └── definition / unit / frequency / lag / revision policy
│
├── LIFECYCLE / CHANGE SIGNALS
│   ├── Revised Table List
│   ├── Discontinued Table List
│   └── Migration Guide
│
├── SEMANTIC NAVIGATION
│   └── Economic & Financial Index and Indicators
│       └── economic concept → official publication table
│
├── OPERATIONS
│   ├── maintenance notices
│   └── portal performance/error telemetry
│
└── EXCLUDED LOOKALIKE
    └── BOT “Open Data” consumer data-sharing initiative
        (not the statistical publication surface)
```

---

# 3. CURRENT MACHINE ACCESS BASELINE

Current BOT API platform:

- Developer Portal: https://portal.api.bot.or.th/
- Gateway: https://gateway.api.bot.or.th/
- Auth header: `Authorization`
- New platform in use since 17 September 2025.

Legacy references include:
- `https://apigw1.bot.or.th/bot/public`
- `X-IBM-Client-Id`

Legacy paths are migration lineage only, not current canonical machine endpoints.

---

# 4. STATISTICS PRODUCT BASELINE

Current Statistics Product exposes:
- `/categorylist`
- `/search-series`
- `/observations`

Current documented Statistics plan:
- quota: unlimited
- rate: 2,000 calls/hour

Observed API spec versions:
- categorylist: v1.0.0
- search-series: v1.0.0
- observations: v1.0.3

Important:
- rate is product/plan scoped, not safely BOT-wide;
- spec version is API scoped, not safely Statistics-wide.

---

# 5. AUTHORITY MATRIX — WHICH SOURCE TO TRUST FOR WHICH QUESTION

| Question | Primary authority | Secondary/verification |
|---|---|---|
| What is the current API endpoint/header? | Current Developer Portal/API docs + Migration Guide | none |
| How do I discover an API series? | search-series / categorylist / official API list | publication title only as candidate clue |
| How do I retrieve machine observations? | observations API | raw retained payload |
| What does an indicator mean? | indicator/table metadata | publication description |
| What value did BOT visibly publish? | BTWS/table/file for that surface/vintage | retained source artifact |
| How do I manually cross-check a value? | BTWS | official publication file |
| Was a publication table replaced/discontinued? | Revised/Discontinued Table lists | catalog evidence |
| What table/file exists? | sector catalog | BTWS/table links |
| What concept maps to which BOT table? | Economic & Financial Index/Indicator page | metadata |
| Is the API under maintenance? | official maintenance/operational notice | connector HTTP evidence |
| What is the canonical internal economic identity? | Thailand Economic OS Canonical Series | source mappings provide evidence |

There is **no single BOT surface that is universal authority for every question**.

---

# 6. IDENTIFIER MODEL

Known identifier namespaces must remain separate.

Examples:

```text
BOT:product:statistics
BOT:api:observations
BOT:table_code:EC_EI_003_S3
BOT:report_id:995
BOT:api_series:<exact code still UNKNOWN>
ThailandOS:series:BOT_PCI_TOTAL
```

Rules:
1. `table_code ≠ report_id ≠ api_series_code` by default.
2. Provider identifiers are external identities.
3. Thailand Economic OS `series_id` is a stable internal canonical identity.
4. Cross-surface mappings require evidence.
5. Same-looking names do not prove same identity.
6. Supersession is a relationship, not an identifier overwrite.

---

# 7. ARCHITECTURE HYPOTHESIS FROZEN FOR DAY 1

The simple model:

`Provider → Product → Series → Observation`

is valid as a local API view but is incomplete for the full provider ecosystem.

Day-1 supported model:

```text
Provider
│
├── Machine Access
│   ├── Source Product
│   ├── Source API
│   └── Provider Series
│
└── Publication Access
    ├── Publication Domain/Catalog
    ├── Publication Table/Report
    └── Source Artifact
        ├── CSV
        ├── XLS/XLSX
        ├── metadata PDF
        ├── HTML snapshot
        └── API spec/raw payload

ProviderSeries / proven publication semantic target
             ↓ evidence-backed mapping
       Canonical Series
             ↓
      Canonical Observation
```

This is a **research hypothesis**, not an authorized database migration.

No V0.1 schema/architecture rewrite is authorized from BOT evidence alone.

The pattern must first be tested against NESDC, TPSO, MOF, and Customs.

---

# 8. SOURCE ROLE MODEL

## Machine acquisition primary
- Statistics `observations`

## Discovery
- `search-series`
- `categorylist`
- official List of Statistics APIs when inspected

## API contract
- API documentation/spec pages

## Semantic metadata
- table/indicator metadata
- BTWS metadata PDF

## Human verification
- BTWS

## Publication catalog
- BOT Statistics sector pages

## Publication artifacts
- CSV
- XLS/XLSX
- PDF metadata
- HTML publication snapshots

## Lifecycle/change signals
- Revised Table List
- Discontinued Table List
- Migration Guide for interface migration

## Semantic bridge
- Economic & Financial Index and Indicators page

## Operational signals
- maintenance notices
- Developer Portal performance/error telemetry

## Fallback candidate
- official CSV/XLS files only after equivalence is proven

## Not an approved fallback
- BTWS HTML

---

# 9. PRIVATE CONSUMPTION INDEX EXAMPLE

Known publication-side objects:

- table_code: `EC_EI_003_S3`
- BTWS report_id: `995`
- title: Private Consumption Index and Components (Seasonally Adjusted)
- frequency: monthly
- base: 2010 = 100
- lag: 1 month
- release schedule: last business day of following month
- revision policy: revised when updated data become available

Observed publication revision evidence:
- an earlier publication snapshot showed JUL 2026 = 171.55 provisional;
- a later publication snapshot showed JUL 2026 = 171.89 revised.

Therefore:
**vintage preservation is empirically necessary**, not merely theoretical.

Exact API series code for PCI total remains UNKNOWN.

---

# 10. LIFECYCLE RULE

Confirmed:
- BOT publication tables/reports can be revised/replaced/discontinued.
- BOT publishes mappings such as Previous Report ID/Name → New Report ID/Name.

Not confirmed:
- equivalent API `series_code` lifecycle.

Canonical Day-1 rule:

```text
Publication table/report lifecycle = CONFIRMED
API series-code lifecycle          = UNKNOWN
```

Never propagate publication-table supersession into API-series supersession without direct evidence.

---

# 11. CONTRADICTION RULES

Day-1 contradiction review established:

- legacy/current API disagreement → resolve by freshness/current API authority;
- table lifecycle vs API-series lifecycle → scope mismatch;
- changed published values → vintage difference, not “bad data”;
- table_code/report_id/series_code → identifier namespace difference;
- product rate differences → configuration scope;
- API version differences → API-level version scope;
- title similarity → candidate mapping only;
- API vs BTWS/file differences → investigate semantics/vintage before choosing;
- publication revision policy + observed revised values → mutually reinforcing evidence.

When official surfaces disagree:
1. retain both raw artifacts;
2. identify namespace/object;
3. verify semantic mapping;
4. compare unit/frequency/adjustment;
5. compare retrieval/publication vintage;
6. inspect p/r status;
7. classify the conflict;
8. never average/overwrite/select by expectation;
9. escalate UNKNOWN conflicts.

---

# 12. CONFIRMED DAY-1 FACTS

1. Current API platform is the new portal/gateway with `Authorization`.
2. Statistics is a distinct BOT API Product.
3. Statistics exposes categorylist, search-series, observations.
4. search-series is an official series-discovery interface.
5. observations retrieves observations using provider series code.
6. An official downloadable List of Statistics APIs exists.
7. Developer Portal controls subscription/application/token workflow.
8. Product-level rate settings differ across BOT products.
9. API spec versions can differ within one product.
10. BOT Statistics website is a separate publication/dissemination ecosystem.
11. Official navigation can remain stale after migration.
12. BOT publishes publication table/report lifecycle changes.
13. BTWS table_code and report_id are distinct identifier namespaces.
14. BOT macro concept pages link concepts to official publication tables.
15. BTWS can serve as official human verification for inspected publication tables.
16. PCI publication values are actually revised across vintages.

---

# 13. SUPPORTED DAY-1 DESIGN CONCLUSIONS

1. BOT must be modeled as a provider with multiple products/surfaces.
2. API Series and Publication Table/Report must remain separate identities.
3. Canonical Series must remain independent of BOT identifiers.
4. Cross-surface mappings require evidence.
5. Authority is question-specific.
6. Official does not mean interchangeable.
7. Verification source is not automatically fallback source.
8. API/file/spec versions and canonical URLs require `last_verified`/version evidence.
9. Raw source disagreement is evidence and must not be silently removed.
10. No production schema migration should happen until the pattern is tested across other P0 providers.

---

# 14. OPEN UNKNOWN REGISTER

## BOT-U01 — List of Statistics APIs direct file URL/type/schema
**Closure:** Day 3 targeted discovery / later targeted gap work.

## BOT-U02 — Exact PCI total API series code
**Closure:** Day 3 search-series + Day 5 dataset selection.

## BOT-U03 — Exact live observations response schema
**Closure:** Day 4 observations research.

## BOT-U04 — Revision/release metadata directly exposed by observations API
**Closure:** Day 4 + Day 6.

## BOT-U05 — BTWS row/table ↔ API series mapping
**Closure:** Day 3/5/6 using exact series + metadata/value comparison.

## BOT-U06 — Rate-limit enforcement scope and live throttle behavior
**Closure:** Day 2 authentication/API behavior.

## BOT-U07 — Stable API spec export URL/history/changelog
**Closure:** Day 2/3 targeted inspection or implementation evidence.

## BOT-U08 — CSV/XLS equivalence to API for fallback
**Closure:** Day 5/6 or later proof.

## BOT-U09 — API series-code lifecycle
**Closure:** Day 6 or explicit BOT series-lifecycle evidence.

No Day-1 freeze claims these UNKNOWNs are solved.

---

# 15. RISKS DISCOVERED

- stale official navigation links;
- legacy examples still circulating;
- product-specific rate/config differences;
- per-API spec-version drift;
- publication-table vs API-series identity confusion;
- revision leakage if vintages are overwritten;
- title-based false mappings;
- file/API fallback assumed without equivalence proof;
- “Open Data” keyword routing to unrelated BOT initiative;
- loss of auditability if source-surface disagreements are normalized away too early.

---

# 16. DO NOT ASSUME

Do **not** assume:

- table_code = report_id;
- report_id = API series code;
- same title = same source identity;
- revised table = revised API series;
- latest value should overwrite earlier published value;
- API is always more current than BTWS/file;
- BTWS is an automatic machine fallback;
- all BOT products share one rate limit;
- all Statistics APIs share one spec version;
- any official BOT link is necessarily current;
- “Open Data” refers to statistical open data;
- Day 1 completion means BOT is complete.

---

# 17. RECOVERY TEST QUESTIONS — ANSWERS MUST BE PRESENT IN THIS FILE

1. **Where is BOT machine access?**  
   Developer Portal/Gateway; Statistics product provides discovery and observations.

2. **Where is human verification?**  
   BTWS/publication surface.

3. **How are API series found?**  
   search-series/categorylist/official API list.

4. **Are table code, report ID, API series code the same?**  
   No. Distinct namespaces; mapping requires evidence.

5. **Does revision happen?**  
   Yes on the publication side; PCI shows real revised vintages. API revision metadata mechanics remain UNKNOWN.

6. **What surfaces describe lifecycle?**  
   Revised/Discontinued Table lists for publication tables/reports.

7. **How are legacy/current APIs separated?**  
   Current Developer Portal/API docs + Migration Guide determine canonical current access; legacy links are aliases/history.

8. **Where does Canonical Series live?**  
   Inside Thailand Economic OS, independent of provider IDs.

9. **What remains UNKNOWN?**  
   BOT-U01..BOT-U09 above.

10. **What comes next?**  
    Day 2 — BOT Authentication & API Behavior. Day-1 closure self-audit has already passed; Day 2 remains planned only and has not started.

---

# 18. DAY-1 BOUNDARY

## Day 1 delivered
- ecosystem map;
- independent revalidation;
- gap hunt;
- architecture challenge;
- source relationship map;
- hardened evidence register;
- contradiction resolution;
- recovery-grade frozen profile.

## Day 1 did not deliver
- live auth behavior;
- exact proof API series;
- observation parser contract;
- full vintage mechanics;
- connector implementation.

---

# 19. HANDOFF

**Day 1 status:** FROZEN v1.1 / GATE PASS  
**Closure audit:** SELF-AUDIT PASS 10/10  
**Current issue:** #11 remains open  
**Next planned research day:** Day 2 — BOT Authentication & API Behavior  
**Day 2 execution status:** PLANNED ONLY / NOT STARTED  
**Implementation hold:** remains active  
**Independent semantic audit:** FUTURE VALIDATION  
**Rule:** UNKNOWN ≠ PASS

Do not reinterpret Day-1 Gate PASS as BOT completion. BOT-U01..BOT-U09 remain open for their assigned later days.
