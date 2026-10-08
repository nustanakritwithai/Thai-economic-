# Day-02 Gap #3 — Official BOT Stat Category Raw OpenAPI Recovered

**Issue:** #11 / Thailand Economic OS V0.2
**Research date:** 2026-10-09 Asia/Bangkok
**Finding:** **OFFICIAL_RAW_OPENAPI_RETRIEVED_AND_PATH_METHOD_VERIFIED**
**Research baseline:** Day-02 Frozen v1 unchanged / Day-02 Gate BLOCKED_CRITICAL_EVIDENCE
**R3 positive auth:** BLOCKED; **R4 full negative behavior:** BLOCKED/PARTIAL.

## 1. Source and verified bytes

**BOT public URL:** https://portal.api.bot.or.th/portal/catalogue-products/statistics-1/d48f73217fdf41995a38859ed2b6e2d5/docs/download

BOT Product page: https://portal.api.bot.or.th/portal/catalogue-products/statistics-1

Tyk vendor documentation describes the `/portal/catalogue-products/{product}/{api}/docs/download` route:
https://tyk.io/docs/5.6/product-stack/tyk-enterprise-developer-portal/api-documentation/list-of-endpoints/portal-1.9.0-list-of-endpoints/

**Actual BOT GitHub-hosted runner acquisition:** [Run 37825476140](https://github.com/nustanakritwithai/Thai-economic-/actions/runs/37825476140), commit `01a10696d63c2df463210c028a9f53ac6b50a4df`. One public GET, HTTP **200**, MIME `application/octet-stream`, **6,799 bytes**, JSON OpenAPI **3.0.1**, Stat Category API info **1.0.0**.

**Official source SHA256:** `282a1ceb6e707e702957eb6d507f04a98dc4be48cc15ec9e1608c81a7c1f2fcd`.

**Raw source preservation:** GitHub Actions Artifact `bot-public-stat-category-spec-37825476140` (artifact ID `11571700056`, 30-day retention). The raw `official-stat-category-openapi.raw` was downloaded from the Action artifact and independently examined/verified byte-for-byte at the SHA above. A full source document was NOT committed to the public repository in this gap; public authoritative source URL, run artifact, digest and nonsecret derived contract are preserved here. No secrets were accessed and no live BOT Gateway/API request was performed in this download step.

## 2. Raw contract, not an interpretation of HTML rendering

The JSON `paths` mapping contains exactly:

| OpenAPI server | HTTP method | Raw OAS relative path | Exact full URL | Documented status keys |
|---|---|---|---|---|
| `https://gateway.api.bot.or.th/categorylist` | **GET** | `/category_list/` | `https://gateway.api.bot.or.th/categorylist/category_list/` | 200 |
| same | **GET** | `/series_list/` | `https://gateway.api.bot.or.th/categorylist/series_list/` | 200 |

The `GET /series_list/` operation requires a `category` query string of type string. This is **published contract**, not proof of live category results or a ready parser. No unauthorized query to the series endpoint was made.

Global OpenAPI `security` references `clientIdHeader`; `components.securitySchemes.clientIdHeader` has **type `apiKey`, name `Authorization`, location `header`**. No actual Token or TOKEN HASH appears in this evidence. No JWT/Bearer conclusions.

The current exported spec enumerates **response 200**, not 401, for either operation. That omission **does not mean** BOT cannot return 401; it means the exact 401 error schema/semantics are **NOT DOCUMENTED in this captured OpenAPI**.

## 3. Important correction to the earlier test

Day-02 Gap #2 queried `GET /categorylist/category_list/get` and observed **HTTP 401** without Authorization. That test response is real but the path was **different from the canonical published OpenAPI path**.

- **Old candidate (not in raw spec):** `https://gateway.api.bot.or.th/categorylist/category_list/get`
- **Current official raw spec GET:** `https://gateway.api.bot.or.th/categorylist/category_list/`

Therefore the earlier 401 **must not** be described as the verified negative auth response of the canonical API operation, despite being a valid observed status at BOT gateway hostname. Exact 401 origin layer, response body and token-validation semantics remain UNKNOWN. The previous historical R4/Gap2 evidence stays immutable and must be amended additively.

## 4. Scope and error interpretation

- **Confirmed:** current public BOT Stat Category v1.0.0 downloadable OpenAPI JSON has canonical Method GET, relative path `/category_list/`, Server base and Header `Authorization`.
- **Partially resolved:** BOT-U07 stable current spec *export* is now demonstrably accessible and hashed. Version-history/changelog, historical diff and update policy remain UNKNOWN.
- **Not confirmed:** actual valid BOT Statistics Token, R3 positive access, whether 401 from an invalid path is due to missing Authorization or routing, the full 401/403/429 error taxonomy, rate/reset behavior and production connector safety.
- **Preserved:** Day-01 Frozen v1.1, Day-02 Frozen v1 and original R3/R4/Gap2 records. Day-02 Gate remains BLOCKED_CRITICAL_EVIDENCE; Issue #11 OPEN.

## 5. Next exact action

Use a separately scoped, no-Token, one-shot read-only GET on the **raw-spec-confirmed** endpoint `https://gateway.api.bot.or.th/categorylist/category_list/` from an authorized egress-enabled runner, retain only safe status/header-presence metadata, and compare with prior 401. Do NOT treat one 401 as a full BOT authorization/error-contract PASS. R3 additionally needs an approved BOT Statistics Token in a secure runner (never copy into chat/GitHub docs).

**UNKNOWN ≠ PASS.**
