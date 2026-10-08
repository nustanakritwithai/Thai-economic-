# Issue #11 — Day 01 Round 7
## BOT Contradiction Resolution

**Date:** 2026-10-08  
**Parent:** Day 01 — BOT Data Ecosystem Map  
**Round:** R7 — Contradiction Resolution  
**Inputs:** R1–R6  
**Goal:** Distinguish real contradictions from scope mismatches, vintage differences, identifier-namespace differences, and unresolved mappings.

---

# RESOLUTION TAXONOMY

R7 classifies apparent conflicts as:

- **TRUE_CONTRADICTION_RESOLVED** — two current statements conflict; one has stronger/current authority.
- **SCOPE_MISMATCH** — both statements are true but govern different objects/questions.
- **VINTAGE_DIFFERENCE** — same semantics, different publication/retrieval vintages.
- **IDENTIFIER_NAMESPACE_DIFFERENCE** — identifiers coexist because they belong to different namespaces.
- **CONFIG_SCOPE_DIFFERENCE** — configuration differs by product/API; not inconsistent.
- **TERMINOLOGY_AMBIGUITY** — labels are broader/looser than the underlying object semantics.
- **UNRESOLVED_MAPPING** — relationship remains unknown and must not be inferred.
- **NO_CONTRADICTION** — claims are compatible.

---

# CR-01 — Legacy BOT API link vs current BOT API platform

## Apparent conflict
Current BOT Statistics navigation exposes BOT API references that can point to different destinations:
- an older navigation path referencing `apiportal.bot.or.th/bot/public`;
- a current BOT API topic link to `portal.api.bot.or.th`.

Meanwhile the current Migration Guide explicitly maps:
- old gateway: `https://apigw1.bot.or.th/bot/public`
- old auth: `X-IBM-Client-Id`
to:
- new gateway: `https://gateway.api.bot.or.th/`
- new auth: `Authorization`.

Official evidence:
- https://www.bot.or.th/en/statistics.html
- https://portal.api.bot.or.th/
- https://portal.api.bot.or.th/migration

## Resolution
**TRUE_CONTRADICTION_RESOLVED at navigation level**

Operational authority order:
1. current API product/spec documentation;
2. Migration Guide;
3. current Developer Portal;
4. generic website navigation.

The legacy URL is retained only as a **LEGACY_ALIAS / migration lineage**.

### Correction to R6 interpretation
BOT-CLM-010 remains useful but is refined:

Do not read it as “the Statistics page only points to the old portal.”

Correct reading:
> The current Statistics page can contain both legacy and current API links in different navigation contexts. Therefore official-site navigation is not sufficient to establish the canonical current machine endpoint.

## Rule
Canonical machine endpoint requires current API-contract evidence, not merely an official-domain hyperlink.

---

# CR-02 — “Discontinued Series” label vs table/report objects

## Apparent conflict
BOT navigation labels some lifecycle content as **Discontinued Series**, while the underlying published items are table-style identifiers such as:
- `EC_EI_027`
- `EC_RL_007`
- `FM_CM_002`

Official evidence:
- https://www.bot.or.th/en/statistics.html
- https://www.bot.or.th/th/statistics/discontinue-table-list.html

## Resolution
**TERMINOLOGY_AMBIGUITY**

For Thailand Economic OS:
- UI/page label “Series” must not be equated to Statistics API `series_code`.
- lifecycle evidence from these pages is classified as **publication table/report lifecycle** unless an API-series relationship is explicitly documented.

## Rule
Object type is determined by evidence structure/identifier context, not page-label wording alone.

---

# CR-03 — Publication table lifecycle vs API-series lifecycle

## Apparent conflict
BOT confirms revised/replaced/discontinued statistical tables, but R6 could not establish equivalent API `series_code` lifecycle.

## Resolution
**SCOPE_MISMATCH + UNRESOLVED_MAPPING**

Both statements can coexist:
- publication table/report lifecycle = CONFIRMED;
- API-series lifecycle = UNKNOWN.

No contradiction exists unless someone incorrectly propagates table lifecycle to API series.

## Rule
Never infer:
`Table superseded → API series superseded`

Require direct API-series lifecycle evidence.

---

# CR-04 — PCI value changed between official publication snapshots

## Observed difference
Official BTWS snapshots for the same PCI table show:

### Snapshot A
Last updated: 31 Aug 2026
- JUL 2026: 171.55 **p**
- JUN 2026: 157.51 **r**
- MAY 2026: 160.18 **r**

### Snapshot B
Last updated: 30 Sep 2026
- AUG 2026: 169.95 **p**
- JUL 2026: 171.89 **r**
- JUN 2026: 157.61 **r**
- MAY 2026: 163.01 **r**

The metadata for `EC_EI_003_S3` explicitly states:
> Revision is made when updated data become available.

Official evidence:
- https://app.bot.or.th/BTWS_STAT/statistics/BOTWEBSTAT.aspx?language=ENG&reportID=995
- https://app.bot.or.th/BTWS_STAT/statistics/DownloadFile.aspx?file=EC_EI_003_S3_ENG.PDF

## Resolution
**VINTAGE_DIFFERENCE — RESOLVED**

This is not inconsistent data. It is evidence of revision across publication vintages.

Canonical interpretation:
```text
JUL 2026 @ 2026-08-31 vintage = 171.55 provisional
JUL 2026 @ 2026-09-30 vintage = 171.89 revised
```

## Rule
Do not overwrite the earlier observation.
Store both vintages and their retrieval/publication context.

This directly validates the V0.1 vintage invariant.

---

# CR-05 — General BOT publication schedule vs PCI-specific release schedule

## Apparent conflict
BOT Statistics publishes a general monthly rule:
- monthly data: last business day of following month, except specified exceptions.

PCI metadata states:
- monthly;
- lag 1 month;
- release schedule: last business day of following month.

Official evidence:
- https://www.bot.or.th/en/statistics.html
- https://app.bot.or.th/BTWS_STAT/statistics/DownloadFile.aspx?file=EC_EI_003_S3_ENG.PDF

## Resolution
**NO_CONTRADICTION**

The PCI-specific metadata is consistent with the general rule.

More general future rule:
> When a table-specific metadata schedule exists, it is more specific and should govern that table over a general publication schedule.

---

# CR-06 — table_code vs report_id vs API series_code

## Apparent conflict
For the inspected PCI publication:
- `table_code = EC_EI_003_S3`
- BTWS URL uses `reportID=995`
- API `series_code` is not yet identified.

## Resolution
**IDENTIFIER_NAMESPACE_DIFFERENCE + UNRESOLVED_MAPPING**

Known:
- table_code and report_id coexist on the publication side.
- they must be separately namespaced.

Unknown:
- relationship from either publication identifier to API `series_code`.

## Rule
Use:
- `BOT:table_code:EC_EI_003_S3`
- `BOT:report_id:995`
- `BOT:api_series:<code>`

Never compare raw identifier strings without namespace.

---

# CR-07 — BOT API product rates differ

## Apparent conflict
Official product pages currently show:
- Statistics: 2,000 calls/hour;
- Exchange Rates: 200 calls/hour;
- Interest Rates: 200 calls/hour.

## Resolution
**CONFIG_SCOPE_DIFFERENCE**

There is no BOT-wide rate contradiction.
The incorrect assumption would be that one provider has one rate limit.

## Rule
Rate configuration belongs at Product/Plan level, and enforcement scope remains a separate UNKNOWN until Day 2.

---

# CR-08 — Statistics APIs have different versions

## Apparent conflict
Current Statistics APIs include:
- search-series v1.0.0;
- observations v1.0.3;
- categorylist v1.0.0.

## Resolution
**CONFIG_SCOPE_DIFFERENCE**

No single “Statistics API version” should be invented.

## Rule
Version key:
```text
provider + product + api_name + spec_version
```

Future raw retrieval evidence should record the relevant API/spec version.

---

# CR-09 — Similar economic title vs proven source identity

## Apparent conflict
The same or similar economic concept can appear in:
- Economic & Financial Indicator pages;
- BTWS table title/rows;
- API search results;
- internal canonical-series naming.

## Resolution
**UNRESOLVED_MAPPING unless explicit evidence exists**

Title similarity is a discovery clue, not identity proof.

## Rule
Allowed:
`title similarity → candidate mapping`

Not allowed:
`title similarity → confirmed mapping`

Confirmation requires exact provider identifier + semantic metadata + value/frequency/unit checks.

---

# CR-10 — API vs BTWS/file values as competing “official truth”

## Apparent conflict
Multiple BOT surfaces can publish values:
- API observations;
- BTWS;
- CSV/XLS files.

All may be official.

## Current evidence state
Exact API series for PCI is not yet identified, so direct API↔BTWS equivalence has not been tested.

## Resolution
**UNRESOLVED_MAPPING / AUTHORITY-SCOPE CONTROL**

Do not declare one surface universally superior.

Current role policy:
- API observations = primary machine-acquisition candidate;
- BTWS = human verification;
- CSV/XLS = official publication artifacts / fallback candidates only.

If values differ after semantics are proven equivalent, first classify:
1. SAME_SEMANTICS_DIFFERENT_VINTAGE
2. PUBLICATION_LAG
3. SOURCE_SURFACE_MISMATCH
4. SEMANTIC_MAPPING_UNCERTAIN
5. UNKNOWN_CONFLICT

Do not overwrite, average, or pick the expected value.

---

# CR-11 — Official statistical “revision policy” vs observed revisions

## Apparent conflict
A policy statement alone might be treated as weaker than observed data changes.

## Resolution
**NO_CONTRADICTION — MUTUALLY REINFORCING**

- metadata says revision occurs when updated data become available;
- BTWS snapshots show actual changes with p/r markers.

The evidence types reinforce each other:
- policy explains expected behavior;
- snapshots prove realized behavior.

## Rule
For vintage-sensitive series, prefer both:
- semantic revision policy;
- empirical retained-vintage evidence.

---

# CR-12 — Publication-table change announcements vs stable canonical economic concepts

## Apparent conflict
BOT can replace/update tables (for example methodology/table changes announced on the Statistics page), while the economic concept itself may continue.

## Resolution
**SCOPE_MISMATCH**

Publication identity can change without requiring Thailand Economic OS to change its internal canonical concept identity.

Example conceptual rule:
```text
old BOT publication object
      ↓ superseded
new BOT publication object
      ↓ evidence-backed mapping
same internal canonical economic concept
```

But mapping is never assumed; semantics must be checked.

## Rule
Canonical series identity should be more stable than source presentation identifiers.

---

# RESOLUTION MATRIX

| Conflict | Classification | Resolution status |
|---|---|---|
| old vs new API navigation | TRUE_CONTRADICTION_RESOLVED | RESOLVED |
| “Discontinued Series” wording vs table IDs | TERMINOLOGY_AMBIGUITY | RESOLVED BY SCOPE |
| table lifecycle vs API-series lifecycle | SCOPE_MISMATCH + UNKNOWN | CONTROLLED UNKNOWN |
| PCI provisional vs revised values | VINTAGE_DIFFERENCE | RESOLVED |
| general vs PCI release schedule | NO_CONTRADICTION | RESOLVED |
| table_code vs report_id vs series_code | NAMESPACE + UNKNOWN | CONTROLLED UNKNOWN |
| Statistics vs FX/IR rate limits | CONFIG_SCOPE_DIFFERENCE | RESOLVED |
| API v1.0.0 vs v1.0.3 | CONFIG_SCOPE_DIFFERENCE | RESOLVED |
| title similarity vs identity mapping | UNRESOLVED_MAPPING | CONTROLLED UNKNOWN |
| API vs BTWS/file “truth” | AUTHORITY SCOPE + UNKNOWN | CONTROLLED UNKNOWN |
| revision policy vs observed revisions | NO_CONTRADICTION | RESOLVED |
| source table changes vs canonical concept | SCOPE_MISMATCH | RESOLVED BY MODEL |

---

# CLAIM REGISTER AMENDMENTS FROM R7

R7 does not rewrite the historical R6 register. It adds interpretation amendments.

## Amendment A — BOT-CLM-010
Refine to:
> Current BOT web navigation contains mixed legacy/current API references in different contexts. Canonical current machine access is determined by current API product/spec documentation and Migration Guide.

## Amendment B — BOT-CLM-011/012
Keep strict separation:
- table/report lifecycle = FACT;
- API-series lifecycle = UNKNOWN.

## Amendment C — BOT-CLM-013/014
Identifier differences are not inconsistencies.
They are separate namespaces with an unproven cross-surface mapping.

## Amendment D — BOT-CLM-016/017
Human-verification and machine-acquisition surfaces can both be official while having different authority scopes.

---

# UPDATED UNKNOWN REGISTER AFTER R7

No critical UNKNOWN is falsely closed.

Still open:
- BOT-U01 — direct URL/file type/schema of List of Statistics APIs
- BOT-U02 — exact API series code for PCI total
- BOT-U03 — exact observations live response schema
- BOT-U04 — revision/release metadata in observations response
- BOT-U05 — BTWS row/table ↔ API series mapping
- BOT-U06 — rate-limit enforcement scope
- BOT-U07 — stable API spec export URL/history
- BOT-U08 — file publication equivalence to API
- BOT-U09 — API series-code lifecycle

R7's job is not to eliminate every UNKNOWN. It ensures UNKNOWNs are no longer disguised as contradictions.

---

# CONTRADICTION HANDLING POLICY FOR CONNECTORS

When official source surfaces disagree:

1. identify exact object/identifier namespace;
2. verify semantic equivalence;
3. compare source surface;
4. compare publication/retrieval vintage;
5. compare unit/frequency/adjustment;
6. inspect provisional/revised status;
7. retain both raw artifacts;
8. classify the conflict;
9. do not normalize to one value until rule/evidence allows it;
10. escalate UNKNOWN conflicts.

Allowed conflict statuses:
- `VINTAGE_DIFFERENCE`
- `PUBLICATION_LAG`
- `SEMANTIC_MAPPING_UNCERTAIN`
- `IDENTIFIER_SCOPE_MISMATCH`
- `LEGACY_CURRENT_CONFLICT`
- `SOURCE_SURFACE_MISMATCH`
- `UNKNOWN_CONFLICT`

---

# ROUND-7 RESULT

**Contradiction Resolution: PASS**

Meaning:
- priority contradiction classes were systematically reviewed;
- genuine current/legacy navigation conflict has an authority-resolution rule;
- false contradictions caused by scope, namespaces, configuration, and vintages were separated;
- unresolved mappings remain explicit UNKNOWNs;
- no official discrepancy was silently erased.

This does **not** close Day 1.

---

# NEXT ROUND

## Round 8 — Day 1 Freeze

Goal:
Freeze the Day-1 BOT Ecosystem Map as a compact, recoverable baseline.

R8 should produce:
1. final Day-1 executive map;
2. confirmed facts;
3. architecture/source-role conclusions;
4. contradiction rules;
5. open UNKNOWNs assigned to Day 2–6 or later rounds;
6. “Do not assume” list;
7. exact handoff to Day 2.

R8 must **not** attempt to solve Day-2 authentication behavior.

---

## Rule

Resolve contradictions by authority scope and evidence, not by preference.  
Different vintage ≠ bad data.  
Different identifier namespace ≠ inconsistent identity.  
Unproven mapping remains UNKNOWN.  
UNKNOWN ≠ PASS.
