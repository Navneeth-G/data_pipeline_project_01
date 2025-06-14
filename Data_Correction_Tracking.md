### Section: **Invalidation & Data Correction Tracking**

This section allows operators and automated tools to flag or trace data that has been invalidated, corrupted, or replaced due to quality issues, external updates, or reruns. These columns play a critical role in managing the reliability and traceability of historical data loads.

---

## 42. `is_invalidated_flag`

**Purpose**
Indicates whether this pipeline run’s data was invalidated after ingestion due to issues such as corruption, schema errors, or upstream problems.

**Why We Need It**

* Allows flagging records for exclusion in analytics or reports.
* Supports rollback workflows or reprocessing logic.
* Helps isolate bad data without deleting historical audit logs.

**Scope**
Can be manually updated or set by validation processes.

**Data Type**: `BOOLEAN`
**Values**:

* `TRUE` – This run’s data has been invalidated
* `FALSE` – Data is considered valid and usable

---

## 43. `is_replacement_run_flag`

**Purpose**
Indicates whether this run was executed to replace or reprocess a previously failed or invalidated load for the same query window.

**Why We Need It**

* Helps distinguish retries from original runs.
* Enables conditional logic for file/table cleanup.
* Maintains lineage of intentional overrides.

**Scope**
Set during pipeline initialization if user or scheduler triggers a correction/replacement.

**Data Type**: `BOOLEAN`
**Values**:

* `TRUE` – This run replaces earlier output for same window
* `FALSE` – Original or independent run

---

## 44. `target_deletion_done_flag`

**Purpose**
Indicates whether the target data corresponding to this run was deleted as part of a cleanup, rollback, or recovery operation.

**Why We Need It**

* Maintains an audit trail for destructive operations.
* Ensures cleanup jobs don’t delete same data twice.
* Supports data re-ingestion pipelines that depend on emptiness.

**Scope**
Typically set after deletion logic is executed by rollback or invalidation code.

**Data Type**: `BOOLEAN`
**Values**:

* `TRUE` – Target data has been deleted
* `FALSE` – Target data still present

---
