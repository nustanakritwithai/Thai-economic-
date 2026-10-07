# Backup & Restore Policy

## Purpose
Project memory is only useful if it can survive account, file, database, or automation failures. Backup is therefore part of auditability, not optional housekeeping.

## Current authoritative layers

### GitHub — engineering source of truth
Contains:
- code;
- schemas;
- release contracts;
- project-control files;
- issues/PR/CI history;
- release snapshots.

Current protection:
- immutable Git commit history;
- explicit release snapshots;
- CI validation of project-control consistency.

Additional external repository backup may be added later; GitHub itself must not be treated as the only possible long-term copy forever.

### Google Drive — human knowledge layer
Contains:
- Master Roadmap;
- long-form plans/reports;
- future executive/cabinet artifacts.

Important project decisions needed for engineering continuity must also be represented in GitHub Decision/Release/Context records. Drive must not be the sole location of an engineering-critical rule.

### Economic Database — future numerical source of truth (V0.4+)
When deployed, the database backup policy becomes mandatory before V0.4 can close.

Minimum future requirements:
- scheduled automated backups;
- point-in-time or versioned recovery where supported;
- documented retention;
- encryption/access controls appropriate to provider;
- restore test against a non-production target;
- recorded restore evidence.

### Raw Data Vault — future source evidence store
Raw official payloads/checksums must be retained according to storage/cost/licensing constraints so normalized observations remain reproducible.

## Recovery priorities
1. Restore project-control truth.
2. Restore schemas/configuration/code.
3. Restore numerical database/vintages.
4. Restore raw source evidence.
5. Restore reports/derived artifacts.
6. Rebuild disposable caches.

## Restore tests
A backup is not considered proven until restore is tested.

Required evidence when relevant:
- backup identifier/time;
- restore target;
- restored version/vintage;
- integrity/checksum result;
- duration;
- failures;
- final PASS/FAIL/UNKNOWN.

## Release gates
- V0.2/V0.3: repository/project-memory continuity must remain reproducible.
- V0.4: database backup + restore test becomes a release-blocking requirement.
- Later production releases: backup/restore evidence must be reviewed at least quarterly or after major storage architecture change.

## Disaster recovery rule
If canonical project state is lost or contradictory:
1. freeze new work;
2. recover latest verified release snapshot;
3. reconcile main SHA/CI;
4. restore PROJECT_STATE / Context Capsule / PM Control;
5. run Drift Review;
6. resume only when one coherent active version/current issue is established.

UNKNOWN ≠ PASS.
