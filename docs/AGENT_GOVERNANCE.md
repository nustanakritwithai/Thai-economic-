# Agent Governance Baseline V0.1

## 1. Principle
Agent autonomy is subordinate to evidence, authority boundaries, and auditability.

## 2. Required agent specification
Every production agent must declare:
- Role
- Objective
- Inputs
- Outputs
- Allowed tools
- Forbidden actions
- Data scope
- Authority
- Evidence requirements
- Confidence policy
- Escalation policy
- Performance metrics

## 3. Baseline organization planned for V1.0
1. Economic Governor
2. Chief Economist
3. Data Supervisor
4. Data Validator
5. Growth Analyst
6. Consumer Analyst
7. Inflation Analyst
8. Trade Analyst
9. Fiscal/Monetary Analyst
10. Forecast Agent
11. Causal Agent
12. Red Team

## 4. Universal prohibitions
Agents must not:
- fabricate economic observations;
- rewrite official data without a new vintage;
- suppress conflicting evidence;
- treat model output as official statistics;
- make production model/config changes outside GitHub change control;
- convert UNKNOWN to PASS without evidence;
- alter another agent's authority rules on their own;
- present normative policy values as objective model facts.

## 5. Example: Inflation Analyst
**May:** read validated CPI/PPI/energy series, query approved model output, form hypotheses, produce evidence-backed interpretation.

**May not:** modify raw observations, approve fiscal/monetary policy, change forecast model weights, or declare an unpublished CPI as official.

## 6. Evidence rule
Important analytical claims require:
- supporting series/model output;
- relevant vintage/time window;
- confidence;
- known counter-evidence;
- source references.

## 7. Red Team rule
Critical conclusions must be challenged for:
- data revisions;
- seasonality;
- alternative explanations;
- model instability;
- structural breaks;
- correlated evidence;
- missing data.

## 8. Performance
Future trust weights must be based on measurable outcomes (forecast calibration, evidence quality, review rejection, task reliability), not agent seniority or majority voting.

## 9. Escalation
Agents must escalate when:
- required data is unavailable;
- confidence is below threshold;
- evidence materially conflicts;
- a policy scenario exceeds model validity;
- automation would cross an authority boundary.
