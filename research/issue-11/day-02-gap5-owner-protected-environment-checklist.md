# Day-02 Gap #5 — BOT R3 owner approval and protected execution gate

**Status:** Metadata-only proof can run; BOT Approved Access, Token and protected runner remain UNVERIFIED until actually evidenced.
**Project:** Thailand Economic OS / V0.2 / Issue #11.
**Day-02 Evidence Gate:** BLOCKED_CRITICAL_EVIDENCE. Frozen v1 historical record unchanged.

## What can be verified automatically and safely

Run the secret-free GitHub workflow .github/workflows/bot-r3-env-metadata.yml. It performs at most two unauthenticated GETs to fixed public GitHub API endpoints to inspect the exact environment name bot-statistics-r3 and, only when applicable, the branch policies. It never calls GitHub Secrets APIs or BOT. Metadata is limited to boolean presence of required reviewers, prevent-self-review, bypass prohibition and branch restriction. It does not log reviewers' names/IDs or raw JSON.

The workflow cannot create the environment or add Secrets: these are owner-level actions not available to the connected GitHub App. GET metadata may return 403/404 when unavailable; then mark UNKNOWN/BLOCKED, not confirmed absence.

## Required human-controlled GitHub setup

1. BOT owner opens https://portal.api.bot.or.th/ -> Profile / My apps / selected Application and verifies Statistics Product 'Approved Access'. Do not share Token, APP ID or a screenshot displaying Credential.
2. Repository administrator opens https://github.com/nustanakritwithai/Thai-economic-/settings/environments and creates exact environment bot-statistics-r3 if absent.
3. Configure Required reviewers with a *different* person/account from the workflow initiator and enable Prevent self-review; if the project has only one maintainer, do NOT fake a second reviewer. Obtain a genuine reviewer or use a separately designed private-runner secret manager approval flow instead.
4. Disable administrator bypass if available; restrict deployment branches/tags to exactly main (not a wildcard) and verify that main is protected and only trusted reviewed code reaches it.
5. Only after protections are verifiably in force, the BOT owner adds the copied real BOT Token directly to an *environment-scoped* secret named BOT_STATISTICS_API_TOKEN, not a repository-wide secret. Never paste Token or TOKEN HASH into ChatGPT/GitHub Issue/commit/PR/log.
6. An independent security reviewer confirms environment protection rules AND the existence (name only) of a Secret. This automatic public probe intentionally does NOT query existence or values of any Secrets.
7. A separate fully reviewed manual-only credential-bearing job/runner would then be approved and deployed; the existing public CI, Pages, network and offline readiness jobs MUST remain secret-free. Live R3 requires a separately authorized one-shot GET and redacted outcome, not mere configuration.

GitHub official guidance: https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments and https://docs.github.com/en/actions/concepts/security/secrets .
BOT official Manual: https://portal.api.bot.or.th/manual .

## Why no credential-bearing job is created

GitHub may allow a workflow that names an unconfigured environment to run without required reviewers. Therefore attaching a Token to a new live workflow before verifying actual approval rules is unsafe. This step adds ONLY metadata discovery and offline tests. Even a public-metadata PASS cannot guarantee Secrets were provisioned or BOT entitlement is approved.

**Next:** real nonsecret metadata receipt -> owner setup only if required -> independent approval -> separately approved privileged R3 run -> additive evidence + Gate reassessment.

UNKNOWN != PASS.
