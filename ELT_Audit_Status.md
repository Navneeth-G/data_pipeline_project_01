### Section: **ELT & Audit Status Indicators**

This section captures the operational and validation states of the pipeline. It includes the processing status of each major phase (ELT), the outcome of audits, and the final status for the overall pipeline run. These fields form the decision layer for retry logic, alerts, and monitoring.

---

## 30. `elt_process_status`

**Purpose**
Describes the current execution status of the pipeline’s extract-load-transform logic.

**Why We Need It**

* Enables operators to monitor whether a job is pending, running, succeeded, or failed.
* Drives DAG progression and conditional branching (e.g., proceed to audit only on `COMPLETED`).
* Used in dashboards and retry systems.

**Scope**
This applies to the entire ELT process, not just extract or load individually.

**Data Type**: `STRING`
**Possible Values**:

* `PENDING` – job not started
* `STARTED` – ELT in progress
* `COMPLETED` – ELT succeeded
* `FAILED` – exception occurred
* `SKIPPED` – stage bypassed due to logic conditions

---

## 31. `audit_process_status`

**Purpose**
Describes the operational status of the audit step.

**Why We Need It**

* Indicates whether audit logic was attempted, completed, or skipped.
* Helps ensure audits were not silently skipped.
* Drives metrics for audit health across pipelines.

**Scope**
Captured after ELT is complete and audit logic begins.

**Data Type**: `STRING`
**Possible Values**: Same as `elt_process_status`

---

## 32. `audit_result_status`

**Purpose**
Captures the outcome of the audit validation performed between source and target (e.g., count comparison, schema check).

**Why We Need It**

* Indicates whether data integrity was preserved during the run.
* Used in dashboards to surface failed or invalid loads.
* Enables suppression of downstream workflows if mismatch is detected.

**Scope**
Should be assigned only if audit was executed (`audit_process_status = COMPLETED`).

**Data Type**: `STRING`
**Possible Values**:

* `MATCHED` – audit passed
* `MISMATCHED` – audit failed (e.g., count mismatch)
* `NOT_VALID` – data insufficient or context invalid

---

## 33. `pipeline_final_status`

**Purpose**
Captures the overall result of the full pipeline run—whether it fully succeeded, failed, or was aborted.

**Why We Need It**

* Enables quick filtering in dashboards and retry queries.
* Aggregates the ELT and audit outcomes into one summarizing field.
* Drives notification and escalation logic.

**Scope**
Should be finalized at the end of the DAG or pipeline script.

**Data Type**: `STRING`
**Possible Values**:

* `PENDING`, `STARTED`, `COMPLETED`, `FAILED`, `SKIPPED`

---

