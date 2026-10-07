# Economic Data Contract V0.1

## 1. Purpose
Define a stable canonical representation so data from different Thai public sources can be ingested, compared, revised, backtested, and audited without changing semantics later.

## 2. Core entities

### Source
Who published the data and how it is accessed.

Required identity:
- `source_id`
- `name`
- `owner`
- `official_url`
- `access_method`
- `priority`

### Series
A stable economic indicator definition.

Required identity:
- `series_id`
- `source_id`
- `name`
- `frequency`
- `unit`
- `seasonal_adjustment`
- `description`

### Observation
A value for one series and economic period.

Required:
- `series_id`
- `period`
- `value`
- `unit`
- `frequency`
- `source_id`
- `release_date`
- `retrieved_at`
- `vintage`
- `revision`
- `quality_status`
- `checksum`

### Quality Event
A validation or data-quality finding linked to an observation/source.

### Prediction
A model output locked before actual outcome is known.

## 3. Series ID convention
`<OWNER>_<INDICATOR>_<DIMENSION>`

Examples:
- `BOT_PCI_TOTAL`
- `BOT_CREDIT_HOUSEHOLD`
- `TPSO_CPI_HEADLINE`
- `NESDC_GDP_REAL`
- `CUSTOMS_EXPORT_TOTAL`
- `MOTS_FOREIGN_ARRIVALS`
- `EPPO_ELECTRICITY_INDUSTRIAL`

IDs are immutable after production use. Renames require aliases/migration; never recycle an old ID for a different meaning.

## 4. Time semantics
- `period` = economic period the observation describes.
- `release_date` = date/time publisher released the value.
- `retrieved_at` = time our system fetched it.
- `vintage` = dataset state available to the system at a point in time.
- `revision` = monotonic revision number within the same observation identity when possible.

These timestamps must never be collapsed into one field.

## 5. Vintage invariant
Historical values are not overwritten. If an official source revises GDP/CPI/etc., store a new vintage and retain the earlier value.

The system must support:
> “What value did we know on date X?”

This is mandatory for honest backtesting.

## 6. Null and UNKNOWN rules
- Missing value ≠ zero.
- Unknown release date must be explicit, not guessed.
- Failed validation must not become a normal observation.
- `UNKNOWN` must remain distinguishable from `VALID`, `WARNING`, and `INVALID`.

## 7. Numeric rules
- Store source value at declared precision.
- Preserve source unit.
- Derived unit conversions create derived records/features; they do not silently replace source values.
- Do not use binary floating behavior as a reason to change published precision; database implementation should use suitable numeric types.

## 8. Quality statuses
Allowed baseline:
- `VALID`
- `WARNING`
- `INVALID`
- `QUARANTINED`
- `UNKNOWN`

## 9. Traceability
Every normalized observation must trace to:
`source_id → retrieval event → raw checksum → parser version → validation result → normalized observation`.

## 10. Change control
Breaking changes to this contract require:
1. Decision Log entry.
2. Schema version bump.
3. Migration plan.
4. Tests.
5. PR review.
