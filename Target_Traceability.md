### Section: **Target Traceability and Developer Notes**

This final section supports traceability of loaded data in external systems (e.g., S3 folder or Snowflake table). It also includes an extensible notes field to store structured or unstructured metadata helpful for debugging, reruns, or manual intervention.

---

## 45. `target_trace_info`

**Purpose**
Stores traceable details about where the output data was loaded—either as a Snowflake WHERE filter or an S3 path pattern.

**Why We Need It**

* Critical for debugging or manually verifying records.
* Helps rollback/delete specific output records without needing re-computation.
* Supports record-level traceability across pipeline runs.

**Scope**
Format depends on target system:

* For S3: `s3://bucket/path/job_id=XYZ/`
* For Snowflake: `WHERE job_id = 'XYZ'` or `tag = 'run_ABC'`

**Data Type**: `STRING` or `VARIANT`
**Examples**:

* `"s3://analytics-pipeline/logs/2025/06/14/job_id=abc123/"`
* `"snowflake_query_hint": "job_id = 'abc123'"`

---

## 46. `misc_info_json`

**Purpose**
Flexible field for storing supplementary structured metadata such as error messages, dynamic parameters, execution flags, responsible engineer, and rerun context.

**Why We Need It**

* Enables richer diagnostics and post-mortem insights.
* Helps developers rerun the pipeline with the exact same context.
* Reduces need for hardcoded overrides or excessive logging elsewhere.

**Scope**
May include runtime context, manual annotations, pipeline config, or error payloads.

**Data Type**: `VARIANT` (JSON-compatible)

**Examples**:

```json
{
  "error": "COPY INTO failed due to file format mismatch",
  "owner": "navneeth",
  "retry_attempt": 2,
  "params_used": {
    "warehouse": "MEDIUM_WH",
    "delta_label": "1 hour"
  }
}
```

---

## 47. `record_inserted_at`

**Purpose**
Timestamp when this row was first inserted into the `pipeline_lifecycle` table.

**Why We Need It**

* Enables tracking when each pipeline run was registered.
* Supports audit trails and insert-time latency measurement.
* Useful for sorting and filtering runs over time.

**Scope**
Should be populated automatically at the time of initial insert.

**Data Type**: `TIMESTAMP`

---

## 48. `record_last_updated_at`

**Purpose**
Captures the latest time this row was modified (e.g., after a retry, audit update, or invalidation).

**Why We Need It**

* Supports change detection and operational alerting.
* Enables tracking run status evolution (e.g., from `STARTED` → `FAILED` → `REPLACED`).
* Required for building dashboards with "last touched" indicators.

**Scope**
Should be updated on every material change to the row (e.g., via `UPDATE` statement or merge logic).

**Data Type**: `TIMESTAMP`

---

## 49. `retry_attempt`

**Purpose**
Tracks how many times this specific query window has been retried after a failure.

**Why We Need It**

* Enables retry logic to incrementally label reruns of the same window.
* Helps identify instability (e.g., windows with frequent failures).
* Used in deduplication and debugging to correlate retries.

**Scope**

* `0` → Original attempt
* `1` or more → Retry attempt number
  Should increment on each retrial of a failed or invalidated window.

**Data Type**: `INTEGER`
**Default**: `0` (first/original attempt)




