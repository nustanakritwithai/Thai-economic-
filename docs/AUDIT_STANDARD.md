# Audit & ID Standard V0.1

## Purpose
Every important artifact must have a stable identity and traceable parentage.

## ID patterns
- Task: `TASK-YYYYMMDD-NNNN`
- Data retrieval/run: `DATA-YYYYMMDD-<SOURCE>-NNN`
- Prediction: `PRED-YYYYMMDD-<TARGET>-NNN`
- Report: `REPORT-YYYYMMDD-NNN`
- Decision: `DEC-NNN`
- Incident: `INC-NNN`
- Model run: `MODEL-YYYYMMDD-<MODEL>-NNN`

## Required lineage

### Data
`Source → Retrieval Event → Raw Checksum → Parser Version → Validation → Normalized Observation`

### Forecast
`Prediction ID → Target → Data Vintage → Feature Set → Model Version → Parameters/Weights → Output → Actual → Error`

### Report
`Report ID → Parent Task(s) → Evidence → Model/State Output → Agent Analysis → Red Team Review → Final Synthesis`

## Audit rules
1. IDs are immutable.
2. Human-readable titles may change; IDs do not.
3. Critical artifacts record creation time and responsible component/agent.
4. No silent mutation of historical prediction output.
5. Corrections append a superseding record/revision.
6. A report without evidence references is not production-ready.
7. An automated action must be reproducible from recorded inputs/configuration whenever technically possible.

## Handoff status vocabulary
- PASS — verified evidence exists.
- FAIL — verified acceptance criterion failed.
- UNKNOWN — not verified.
- BLOCKED — cannot verify/complete because a named dependency is unresolved.

UNKNOWN is not PASS.
