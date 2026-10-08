# Day-02 Gap #3 — Raw BOT OpenAPI and One Canonical No-Token HTTP Response

**Project:** Thailand Economic OS / V0.2 / Issue #11 OPEN
**Date:** 2026-10-09 (Asia/Bangkok)
**Finding:** Publisher's raw Stat Category OpenAPI **confirms GET /category_list/** and **GET /series_list/**. One separate no-token request to the canonical GET returned **HTTP 401**.
**Day-02 Gate:** BLOCKED_CRITICAL_EVIDENCE; R3 positive authentication BLOCKED; R4 full error taxonomy PARTIAL/BLOCKED.

## Verified official OpenAPI bytes

- Official download: https://portal.api.bot.or.th/portal/catalogue-products/statistics-1/d48f73217fdf41995a38859ed2b6e2d5/docs/download
- [BOT spec retrieval run 37825476140](https://github.com/nustanakritwithai/Thai-economic-/actions/runs/37825476140) was HTTP 200, public `application/octet-stream`, 6,799 bytes, valid OpenAPI 3.0.1, info version 1.0.0.
- Raw SHA256: `282a1ceb6e707e702957eb6d507f04a98dc4be48cc15ec9e1608c81a7c1f2fcd`.
- Git-archived official public raw document, deterministic gzip: [`research/issue-11/official-snapshots/BOT_Stat_Category_OpenAPI_v1.0.0_2026-10-09.json.gz`](https://github.com/nustanakritwithai/Thai-economic-/blob/main/research/issue-11/official-snapshots/BOT_Stat_Category_OpenAPI_v1.0.0_2026-10-09.json.gz); 1,483 bytes, gzip SHA256 `663895274a24012b0bd816c32a6d72dea39fff37626f17c4036bc5ac67f82b48`, Git blob `efe133af498bc58bd31654e15943d74da535b322`.
- Unpack/verify: `gzip -dc research/issue-11/official-snapshots/BOT_Stat_Category_OpenAPI_v1.0.0_2026-10-09.json.gz | sha256sum` must produce the raw checksum above. Source manifest: `research/issue-11/official-snapshots/BOT_Stat_Category_OpenAPI_v1.0.0_2026-10-09.manifest.json`.
- This is a public official spec snapshot obtained on the date above; BOT changelog/history and future revisions are still unknown (BOT-U07 PARTIAL).

## Canonical source contract

| API base | Method | Relative path | Query | Official response statuses |
|---|---|---|---|---|
| `https://gateway.api.bot.or.th/categorylist` | GET | `/category_list/` | none required | 200 |
| same | GET | `/series_list/` | required `category` string | 200 |

Global security scheme `clientIdHeader` is `apiKey` via header `Authorization`. The captured OpenAPI does **not** specify a 401 error response. This is **not proof that 401 cannot occur**, and it does not define the meaning of a 401.

## Actual response on canonical GET (separate controlled run)

[GitHub canonical no-Authorization GET run 37826019253](https://github.com/nustanakritwithai/Thai-economic-/actions/runs/37826019253) executed exactly one GET to `https://gateway.api.bot.or.th/categorylist/category_list/`, **without a Token**.

| Actual measurement | Observation |
|---|---|
| UTC response observed | `2026-10-08T18:39:57.776209+00:00` |
| HTTP status | **401** |
| Sanitized Content-Type | `application/json` |
| HTTP Content-Length header | 46 bytes, NOT measured raw body size |
| GitHub-runner total request elapsed | 1002.99 ms |
| Request count / retries / redirects | 1 / 0 / 0 |
| Authorization / request body / response body read | NO / NONE / NO |
| Response raw headers/content logged | NO; safe header presence flags only |

Canonical run unit tests 6/6 PASS. GitHub Actions ZIP artifact `bot-canonical-noauth-37826019253` contains the actual sanitized JSON; its extracted JSON SHA256 `26d132cdec360d751c02261ff7a3b06b4443b9329c9069c6d015312cf30a54b6` was independently verified against log-derived evidence.

**Strict interpretation:** one no-Authorization GET at a current publisher-documented URL returned HTTP 401. We cannot establish whether gateway/edge/WAF or upstream application issued it or what the unrecorded JSON error body says. The OAS only documents 200. No full BOT 401/403/429 error mapping or credential success can be inferred.

## Preserve historical original results

- Initial R4 runner failed local DNS (curl 6), *zero* origin HTTP; its historical record remains unchanged.
- Gap2 candidate `/category_list/get` returned 401, but **that path does not appear in the recovered OAS**.
- Gap3 canonical `/category_list/` returned 401, *this path and GET are confirmed by recovered OAS*. Both measured statuses are actual, but different request paths.
- Do not backfill old R4 `null` statuses with 401, close R3 or assert a provider-specific authentication failure policy.

## What's still blocked

`BOT-R3-CRED-01` remains OPEN (approved usable Statistics Token absent from trusted test runner). `BOT-R4-EGRESS-01` remains OPEN for the original DNS context and full provider-specific negative/error behavior (401 cause and other classes). BOT-U07 stable raw *current* export solved partially, but historical versions/changelog not proven; keep that unknown with a qualified status. Security model remains design-only; rate enforcement and maintenance contradiction still open.

**Next:** approved BOT Statistics access/protected one-shot R3 positive test, then BOT-backed clarification of 401 semantics and other narrowly safe R4 cases. Keep V0.2 production connector HOLD, Day-02 Frozen v1 unchanged, Day-02 evidence Gate BLOCKED and Issue #11 OPEN.

**UNKNOWN ≠ PASS.**
