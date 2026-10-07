# Source Registry V0.1

This file defines the initial public-data acquisition scope. Registration does not mean the connector is implemented.

| Source ID | Owner | Domain | Typical frequency | Access | Priority | Revision possible | V0.2 |
|---|---|---|---|---|---|---|---|
| BOT | Bank of Thailand | monetary, credit, FX, consumption/investment indicators | daily–monthly | API/files | P0 | yes | planned |
| NESDC | National Economic and Social Development Council | GDP/national accounts | quarterly | CSV/XLS/files | P0 | yes | planned |
| TPSO | Trade Policy and Strategy Office / MOC | CPI/PPI/prices | monthly | API/files | P0 | yes | planned |
| MOF | Ministry of Finance | revenue, tax, fiscal | monthly–quarterly | API/files | P0 | yes | planned |
| CUSTOMS | Thai Customs | imports/exports/HS-country trade | monthly | CSV/files | P0 | yes | planned |
| NSO | National Statistical Office | household, labor, demographics | mixed | files/API where available | P1 | yes | selected |
| MOTS | Ministry of Tourism and Sports | tourism | monthly | files | P1 | yes | later |
| EPPO | Energy Policy and Planning Office | energy/electricity/fuels | daily–monthly | files/API | P1 | yes | later |
| OAE | Office of Agricultural Economics | agriculture/prices | daily–monthly | API/files | P1 | yes | later |
| PDMO | Public Debt Management Office | public debt | monthly | CSV/XLS | P1 | yes | later |
| SET_SEC | SET / SEC | capital market | daily–monthly | API/files | P1 | varies | later |

## Registry fields required before connector implementation
- source_id
- canonical owner/name
- official_url
- data/license terms
- access method
- expected cadence
- expected release lag
- revision behavior
- authentication requirement
- parser owner
- fallback behavior
- last verified date

## Priority meaning
- **P0:** required for first national measurement/forecast foundation.
- **P1:** important expansion once core ingestion is stable.
- **P2:** experimental/alternative data; must not block core releases.

## V0.2 rule
Do not add every available dataset. Start with a small, high-value set from each P0 source and prove ingestion, vintage, validation, and audit behavior end-to-end.
