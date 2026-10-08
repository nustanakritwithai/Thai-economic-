# Day-02 Gap #3 — Retrieve official BOT Stat Category OpenAPI specification

**Status:** research probe prepared; actual HTTP/parsed-spec outcome must be read from GitHub Actions.
**Gate:** BLOCKED_CRITICAL_EVIDENCE. Frozen v1 and R3/R4 history remain unchanged.

BOT Statistics official documentation: https://portal.api.bot.or.th/portal/catalogue-products/statistics-1/d48f73217fdf41995a38859ed2b6e2d5/docs
Official Tyk developer portal endpoint reference: https://tyk.io/docs/5.6/product-stack/tyk-enterprise-developer-portal/api-documentation/list-of-endpoints/portal-1.9.0-list-of-endpoints/
Exact one-shot public download candidate: https://portal.api.bot.or.th/portal/catalogue-products/statistics-1/d48f73217fdf41995a38859ed2b6e2d5/docs/download

The public web reader recognized application/octet-stream but did not decode a spec. This is a lead, not a verified method/path.
Run exactly one GET to BOT Portal public docs/download (NOT gateway) with default CA and hostname TLS, no Token, no follow-up, no redirect, no retry and a 2MB size cap.
Parse JSON or YAML if parser is installed. If valid OpenAPI, preserve bytes+SHA256 in Actions artifact (not source control) and emit only safe Operation Method/Path/Server/Security Scheme metadata.
If not valid OpenAPI or denied, keep raw Method/Path UNKNOWN and record observed status without guessing.
Even an official raw GET operation does not show whether BOT issued an observed 401 due to missing token; no response body or new gateway request in this task.

**UNKNOWN ≠ PASS.**
