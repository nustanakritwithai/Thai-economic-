# Issue #11 — Day 01 Research Log
## BOT Data Ecosystem Map

**Date:** 2026-10-08  
**Active release:** V0.2 Core Data Connectors  
**Issue:** #11 — Inventory official P0 data endpoints  
**Plan:** docs/V0.2_ISSUE11_28_DAY_RESEARCH_PLAN.md  
**Status:** DAY 01 COMPLETE — findings frozen for Day 1 only

---

## QUESTION

What are the authoritative Bank of Thailand (BOT) entry points relevant to V0.2, and how are machine access, human verification, statistical metadata, and source-change signals separated?

Day 1 intentionally does **not** finalize:
- exact authentication/error behavior;
- exact search-series parameters/response schema;
- exact observations parameters/response schema;
- exact proof series code;
- revision/vintage mechanics.

Those belong to later planned days.

---

## METHOD

1. Reviewed the official BOT Developer Portal and Statistics API product.
2. Reviewed official documentation pages for:
   - Stat Category;
   - Search Stat APIs / search-series;
   - Observations.
3. Reviewed BOT API migration guide and user manual.
4. Reviewed BOT public Statistics landing page and publication/discontinued-series resources.
5. Inspected official BOT Web Statistics tables as a human-readable verification surface, including the current Private Consumption Index table.
6. Checked BOT API product catalogue to identify whether economically relevant APIs are all inside the Statistics product or split across products.

Only official BOT domains were treated as authoritative evidence:
- bot.or.th
- portal.api.bot.or.th
- gateway.api.bot.or.th
- app.bot.or.th

---

## EVIDENCE

### E1 — BOT API portal
https://portal.api.bot.or.th/

Finding:
- BOT's new API system is the current machine-access entry point.
- The portal states the new system has been available since 17 September 2025.
- Developer Portal: https://portal.api.bot.or.th/
- Gateway: https://gateway.api.bot.or.th/

### E2 — Statistics product
https://portal.api.bot.or.th/portal/catalogue-products/statistics-1

The Statistics product currently exposes three REST API families:
1. **Stat Category** — listen path `/categorylist`
2. **Observations** — listen path `/observations`
3. **search-series** — listen path `/search-series`

The product page currently states:
- Statistics Plan quota: unlimited
- Rate: 2,000 calls / 1 hour

Rate/auth details are recorded as Day-1 evidence but remain scheduled for deeper Day-2 verification.

### E3 — Stat Category documentation
https://portal.api.bot.or.th/portal/catalogue-products/statistics-1/d48f73217fdf41995a38859ed2b6e2d5/docs

Official API base:
https://gateway.api.bot.or.th/categorylist

Documented operations include:
- category list
- series list

Interpretation:
This is the structured browse/discovery route when navigating by BOT statistical categories rather than free-text search.

### E4 — Search Stat APIs documentation
https://portal.api.bot.or.th/portal/catalogue-products/statistics-1/e581631f50164ffc72525b11050b5744/docs

Official API base:
https://gateway.api.bot.or.th/search-series

The documentation states search can use:
- series code;
- series name;
- relevant keywords.

The service displays up to 100 series per search.

Interpretation:
This is the likely primary route for discovering exact official series identifiers during V0.2.

### E5 — Observations documentation
https://portal.api.bot.or.th/portal/catalogue-products/statistics-1/e2dcfd41460e49a86276db01aeb3cd1f/docs

Official API base:
https://gateway.api.bot.or.th/observations

The documentation states observations are selected by official series code.

Interpretation:
Expected machine path is:
`discover series → obtain exact series code → request observations`.

Exact request/response behavior is deferred to Day 4.

### E6 — Migration guide
https://portal.api.bot.or.th/migration

The official migration guide documents an important architecture break:

Old:
- Gateway: `https://apigw1.bot.or.th/bot/public`
- Auth header: `X-IBM-Client-Id`

New:
- Gateway: `https://gateway.api.bot.or.th/`
- Auth header: `Authorization`

Interpretation:
Any legacy examples found online must be treated as potentially obsolete unless reconciled with the new portal.

### E7 — BOT API manual
https://portal.api.bot.or.th/manual

The manual documents the operational flow:
`create account → subscribe to API product/plan → create/select application → approval/access → use token`.

This confirms that the Developer Portal is not just documentation; it is also the current credential/subscription management surface.

Detailed auth behavior remains Day 2 work.

### E8 — BOT public statistics landing page
https://www.bot.or.th/en/statistics.html

The official Statistics site provides:
- multiple statistics domains;
- BOT API link;
- publication schedules;
- standards/revision material;
- discontinued-series links;
- direct links to statistical tables.

The general publication schedule states:
- daily: every business day;
- weekly: last business day of following week;
- monthly: last business day of following month unless otherwise specified;
- quarterly: last business day of following quarter unless otherwise specified;
- yearly: last business day of following year unless otherwise specified.

Individual tables may have specific release schedules.

### E9 — BOT Web Statistics / BTWS
Example current Private Consumption Index table:
https://app.bot.or.th/BTWS_STAT/statistics/BOTWEBSTAT.aspx?language=ENG&reportID=995

Observed capabilities:
- human-readable values;
- date range;
- last-updated timestamp;
- unit/base;
- Download;
- Metadata;
- provisional/revised markers such as `p` and `r`.

Current PCI table:
- table code: `EC_EI_003_S3`
- title: Private Consumption Index and Components (Seasonally Adjusted)
- current web table covers Jan 2010 onward;
- August 2026 is shown as provisional at the time checked;
- prior months contain revised markers.

Interpretation:
BTWS is a strong **human verification and metadata surface** even if our production connector ultimately uses BOT API.

### E10 — PCI metadata PDF
https://app.bot.or.th/BTWS_STAT/statistics/DownloadFile.aspx?file=EC_EI_003_S3_ENG.PDF

The official metadata states:
- table code: EC_EI_003_S3;
- monthly frequency;
- one-month lag;
- release schedule: last business day of following month;
- revision policy: revision is made when updated data become available.

This is strong evidence that revision/vintage handling will matter later.

Day 6 will investigate how those revisions appear in machine-access data and how to preserve vintages.

### E11 — Revised/discontinued series resources
https://www.bot.or.th/en/statistics/revised-table-list.html
https://www.bot.or.th/en/statistics/discontinue-table-list.html

BOT explicitly publishes:
- revised/replaced table mappings;
- discontinued statistical tables.

Interpretation:
Series/table identity is not permanently static. Connector/source-registry design must allow supersession/replacement relationships rather than silently reusing identifiers.

### E12 — API product catalogue
https://portal.api.bot.or.th/portal/catalogue-products

Finding:
Not every economically relevant BOT API is contained under the generic Statistics product.

Examples of separate products include:
- Exchange Rates;
- Interest Rates;
- Debt Securities Auction;
- Others.

Interpretation:
The future BOT integration layer should model BOT as a **provider with multiple products**, not as one monolithic endpoint.

For Issue #11's first proof, the PCI/statistics path remains the intended focus.

---

## FINDING

### BOT ecosystem map

```text
Bank of Thailand
│
├── Public Statistics Website
│   ├── statistics domains/categories
│   ├── publication schedule
│   ├── standards / revision policy
│   ├── revised-series mappings
│   └── discontinued-series mappings
│
├── BOT Web Statistics (BTWS / app.bot.or.th)
│   ├── human-readable statistical tables
│   ├── Download
│   ├── Metadata
│   ├── Last Updated
│   └── provisional/revised markers (p/r)
│
└── BOT Developer Portal
    ├── Product Catalogue
    │
    ├── Statistics product
    │   ├── categorylist
    │   │   ├── category list
    │   │   └── series list
    │   │
    │   ├── search-series
    │   │   └── keyword/code/name → candidate series
    │   │
    │   └── observations
    │       └── series code → observations
    │
    ├── Exchange Rates product
    ├── Interest Rates product
    ├── Debt Securities Auction product
    └── other products
```

### Expected Statistics acquisition path

```text
BOT Developer Portal / Statistics product
        ↓
categorylist OR search-series
        ↓
exact official series code
        ↓
observations
        ↓
raw API payload
        ↓
future V0.2 raw artifact layer
```

### Human verification path

```text
BOT API observation
        ↕ cross-check
BOT Web Statistics table
        +
table metadata PDF
        +
publication/revision resources
```

---

## CONFIDENCE

### HIGH
- Current Developer Portal base URL.
- Current API Gateway base.
- Statistics product exists and exposes categorylist/search-series/observations.
- Search-series is an official series-discovery mechanism.
- Observations uses series code.
- BTWS remains an official human-readable statistics surface.
- BOT publishes explicit revised/discontinued-series information.
- The new API architecture replaced the old gateway/header model.

### MEDIUM
- BTWS should be used as our default manual cross-check surface for Statistics API values.
  - Strongly supported operationally, but exact one-to-one API/web-table mapping must be proven for the selected series.

### NOT YET VERIFIED / UNKNOWN
- Exact current query parameters for all three Statistics endpoints.
- Exact response schemas/field names in live calls.
- Whether every BTWS table has a corresponding Statistics API series.
- Exact Statistics API series code for the current PCI total.
- Whether Observations exposes revision/release metadata directly.
- Whether the downloadable API series list has a stable machine URL.
- Whether BTWS Download itself has a stable automation-friendly URL.
- Exact authentication failure modes / approval latency / token behavior.
- Whether product quotas/rates can vary by subscription/account over time.

---

## IMPACT

### 1. Provider ≠ Product
BOT must be represented as one provider with multiple API products.

Do not design:
`BOT → one endpoint`

Prefer:
`BOT provider → product → API/series`.

### 2. Discovery must be first-class
Exact series IDs should be discovered from official BOT mechanisms and persisted in the Source/Series registry.

Never guess a series code from table names.

### 3. Legacy examples are dangerous
Any code using:
- `apigw1.bot.or.th/bot/public`
- `X-IBM-Client-Id`

must be treated as legacy unless a specific migration reason exists.

### 4. Human cross-check is part of verification
For the first BOT proof, API values should be checked against:
- BTWS table;
- table metadata;
- update/revision markers.

### 5. Series lifecycle matters
BOT's revised/discontinued table resources imply future source metadata should support:
- active;
- revised/replaced;
- discontinued;
- superseded-by relationship.

### 6. Vintage work is unavoidable
The current PCI table already displays revised observations and the metadata explicitly allows revision when updated data become available.

This reinforces the V0.1 decision that historical vintages must not be overwritten.

---

## DAY-1 STATUS

| Dimension | Status | Note |
|---|---|---|
| Official authority | PASS | BOT official domains identified |
| Machine entry point | PASS | Developer Portal + gateway |
| Statistics product map | PASS | categorylist/search-series/observations |
| Human verification surface | PASS | BOT Statistics + BTWS |
| Migration awareness | PASS | old vs new gateway/header documented |
| Source-change signals | PASS | revised/discontinued resources identified |
| Exact auth behavior | UNKNOWN | Day 2 |
| Exact series code | UNKNOWN | Day 3/5 |
| Exact observation schema | UNKNOWN | Day 4 |
| Revision/vintage machine behavior | UNKNOWN | Day 6 |

**Day 1 result: PASS for ecosystem mapping.**

This does **not** mean BOT Source Profile or Issue #11 is PASS.

---

## NEXT QUESTION

### Day 2 — BOT Authentication & API Behavior

Answer with evidence:

1. What exact account/subscription/application approval flow is required today?
2. What exactly must be sent in the `Authorization` header?
3. What happens for missing/invalid credentials?
4. What rate-limit/quota signals are exposed?
5. Are rate limits enforced per app/token/product?
6. What error status/body patterns must a future connector classify?
7. What secret-handling rules should V0.2 enforce?

Do not start Day 3 until Day 2 findings are frozen.

---

## Rule

Official source first.  
UNKNOWN ≠ PASS.  
Day completion does not advance V0.2 by itself.
