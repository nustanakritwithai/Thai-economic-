# Architecture V0.1

Status: **BASELINE — V0.1**

## 1. System objective
Thailand Economic OS separates numerical truth, analytical models, agent reasoning, and human policy authority.

```text
PUBLIC DATA SOURCES
        ↓
CONNECTORS
        ↓
RAW DATA VAULT
        ↓
VALIDATION
        ↓
NORMALIZATION
        ↓
ECONOMIC DATABASE + VINTAGES
        ↓
CALCULATION / FEATURE ENGINE
        ↓
ECONOMETRIC + ML MODELS
        ↓
ECONOMIC STATE / FORECASTS
        ↓
MULTI-AGENT ORGANIZATION
        ↓
RED TEAM / AUDIT
        ↓
REPORTS / POLICY SIMULATION
        ↓
HUMAN DECISION
```

## 2. Authority boundaries

| Component | May create | Must not do |
|---|---|---|
| Connector | Raw source snapshots | Interpret economics |
| Validator | Quality status | Rewrite source values silently |
| Normalizer | Canonical observations | Delete historical vintages |
| Calculation engine | Derived metrics | Invent missing raw values |
| Forecast model | Model forecasts | Present forecast as official statistic |
| LLM/Agent | Interpretation, hypothesis, report | Directly alter raw observations or official values |
| Red Team | Challenges, counter-evidence | Hide disagreement |
| Human | Objectives, policy/value decisions | Bypass audit trail for production changes |

## 3. Storage layers
1. **Raw Data Vault** — immutable source payloads and checksums.
2. **Economic Database** — normalized series, observations, metadata, vintages.
3. **Knowledge Graph** — economic relationships with evidence/confidence.
4. **Research Memory** — hypotheses and analytical findings.
5. **Prediction Ledger** — forecasts locked before actual outcomes.
6. **Audit Ledger** — tasks, models, revisions, reports, incidents.

## 4. Operating infrastructure
- **GitHub:** engineering truth; code, schemas, issues, PRs, CI, version history.
- **PostgreSQL/Supabase:** numerical truth and runtime state.
- **Google Drive:** human-readable plans, reports, policy briefs.
- **Google Calendar:** data release dates and organizational cadence.
- **Gmail:** inbound bulletins, outbound alerts/reports.
- **AI Scheduler:** daily/weekly/monthly organizational tasks.
- **Server cron/event bus:** high-frequency or pipeline-critical triggers.

## 5. Core event flow
```text
SOURCE_UPDATE
  → ingest
  → validate
  → normalize
  → DATA_UPDATED event
  → affected calculations
  → affected forecasts
  → domain-agent analysis
  → Red Team
  → Chief Economist synthesis
  → Economic Governor brief
  → archive + audit
```

## 6. Reliability rules
- Idempotent ingestion.
- Immutable vintages.
- Explicit UNKNOWN state.
- Every derived value traces to source observations.
- Every forecast stores model/data version.
- Every critical report contains evidence and uncertainty.
- Automation failures must surface; silent failure is prohibited.

## 7. V0.1 freeze rule
Changes to authority boundaries, observation identity, vintage semantics, or audit lineage after V0.1 require a documented Decision Log entry and reviewed pull request.
