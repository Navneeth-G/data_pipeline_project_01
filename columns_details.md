## Column: `run_source`

**Purpose**
Identifies who or what triggered this pipeline run. This is essential to distinguish automated runs (e.g., via Airflow) from ad hoc or manual ones. It helps audit how the run was initiated and by whom.

**Data Type**
`STRING`

**Possible Values**

* `airflow`
* `manual`
* `cli`
  (Extendable for other orchestrators like `az-data-factory`, etc.)

---

## Column: `job_id`

**Purpose**
Provides a unique identifier for each run of the pipeline. It links all records, logs, and audit metrics associated with a single execution unit.

**Data Type**
`STRING`

**Possible Values**

* `JOB_20250613_001`
* UUID or timestamp-based identifiers (e.g., `f2c71b3e-88d4...`)

---

## Column: `source_name`

**Purpose**
Specifies the type of data source system involved in this pipeline (e.g., Elasticsearch, MySQL, S3). Helps determine extraction logic and toolchain.

**Data Type**
`STRING`

**Possible Values**

* `elasticsearch`
* `mysql`
* `s3`
* `kafka`

---

## Column: `data_domain`

**Purpose**
Categorizes the data within a logical or business context. Useful for separating logs, metrics, transactions, etc., and grouping related pipelines.

**Data Type**
`STRING`

**Possible Values**

* `logs`
* `metrics`
* `clickstream`
* `user_profiles`

---

## Column: `source_object`

**Purpose**
Denotes the specific table, index, or file name being accessed in the source system. This enables fine-grained tracking of what exact data was handled.

**Data Type**
`STRING`

**Possible Values**

* `logs-prod-*`
* `user_data_table`
* `raw/2025/06/13/events.json`

---

## Column: `source_data_frequency`

**Purpose**
Describes how frequently the source system generates new data. This helps estimate expected volume, schedule ingestion, and design monitoring thresholds.

**Data Type**
`STRING`

**Possible Values**

* `1 MIN`
* `5 MIN`
* `1 HOUR`
* `DAILY`

---

## Column: `collection_frequency`

**Purpose**
Indicates how often the pipeline is configured to ingest or collect data from the source. Used to align extraction windows with upstream data flow.

**Data Type**
`STRING`

**Possible Values**

* `15 MIN`
* `1 HOUR`
* `DAILY`

---

## Column: `query_window_start_at`

**Purpose**
Marks the beginning of the time window for which data is extracted. This allows controlled slicing of source data, especially when handling large volumes or historical loads.

**Data Type**
`TIMESTAMP`

**Possible Values**

* `2025-06-13T00:00:00Z`
* ISO 8601 timestamp in UTC

---

## Column: `query_window_end_at`

**Purpose**
Marks the end of the data extraction time window. Defines the upper bound of the time range to be ingested in a given run.

**Data Type**
`TIMESTAMP`

**Possible Values**

* `2025-06-13T01:00:00Z`
* ISO 8601 timestamp in UTC

---

## Column: `query_window_delta_label`

**Purpose**
A human-readable label that describes the size of the query window. Helps with understanding batch size and standardizing run intervals across pipelines.

**Data Type**
`STRING`

**Possible Values**

* `15 MIN`
* `1 HOUR`
* `1 DAY`

---

## Column: `pipeline_route`

**Purpose**
Describes the route the data takes from source to target. Helps track whether intermediate stages (e.g., S3) are used or if it is a direct load.

**Data Type**
`STRING`

**Possible Values**

* `source_to_snowflake`
* `source_to_s3_to_snowflake`
* `source_to_target`

---

## Column: `job_started_at`

**Purpose**
Indicates when the execution of this pipeline run officially started. It serves as the main time anchor for auditing and duration calculations.

**Data Type**
`TIMESTAMP`

**Possible Values**

* `2025-06-13T01:10:00Z`
* ISO 8601 timestamp in UTC

---

## Column: `source_count_pre_checked_at`

**Purpose**
Timestamp when the pre-extraction count was measured at the source. This helps confirm the expected volume before actual data pull begins.

**Data Type**
`TIMESTAMP`

**Possible Values**

* `2025-06-13T01:11:00Z`

---

## Column: `source_count_pre_extract`

**Purpose**
Number of records present in the source system when the pre-check was performed. Used to validate stability and ensure no drift before extraction.

**Data Type**
`INTEGER`

**Possible Values**

* `10000`
* `0` (if source was empty)

---

## Column: `source_extracted_at`

**Purpose**
Timestamp indicating when the extraction step finished. Used to track the exact point data was pulled from the source.

**Data Type**
`TIMESTAMP`

**Possible Values**

* `2025-06-13T01:13:00Z`

---

## Column: `source_extracted_count`

**Purpose**
The actual number of records extracted from the source during this pipeline run. This value is compared against both source pre/post counts and target load.

**Data Type**
`INTEGER`

**Possible Values**

* `10000`

---

## Column: `source_count_post_checked_at`

**Purpose**
Timestamp when the post-extraction count was re-measured. Used to detect if data at source changed during/after extraction.

**Data Type**
`TIMESTAMP`

**Possible Values**

* `2025-06-13T01:15:00Z`

---

## Column: `source_count_post_extract`

**Purpose**
Number of records present at source after extraction. Useful to validate immutability or volatility of source data across the extraction window.

**Data Type**
`INTEGER`

**Possible Values**

* `10000` (stable)
* `10010` (source changed)

---

## Column: `source_to_target_started_at`

**Purpose**
Marks when the transfer from source to target (e.g., S3 or Snowflake) began. This helps diagnose delays or measure performance of the staging/load layer.

**Data Type**
`TIMESTAMP`

**Possible Values**

* `2025-06-13T01:16:00Z`

---

## Column: `source_to_target_ended_at`

**Purpose**
Marks when the transfer from source to target completed. Paired with the start time, this allows computation of the total transfer duration.

**Data Type**
`TIMESTAMP`

**Possible Values**

* `2025-06-13T01:18:00Z`

---

## Column: `source_to_target_duration_mins`

**Purpose**
Duration in minutes taken to move data from source to target. This field supports performance tracking and SLA validation.

**Data Type**
`FLOAT`

**Possible Values**

* `2.0`
* `15.5`

---

## Column: `target_loaded_at`

**Purpose**
Indicates the exact time the target system (e.g., Snowflake) confirmed that data was successfully loaded. This is essential for auditing data freshness and downstream triggers.

**Data Type**
`TIMESTAMP`

**Possible Values**

* `2025-06-13T01:18:00Z`

---

## Column: `extract_to_load_gap_mins`

**Purpose**
Represents the delay between when data was extracted and when it was fully loaded into the target. Used to diagnose latency between stages.

**Data Type**
`FLOAT`

**Possible Values**

* `5.0`
* `0.0`

---


## Column: `target_loaded_count`

**Purpose**
Specifies how many records were successfully loaded into the target system (e.g., Snowflake). This is the primary metric for validating ingestion success.

**Data Type**
`INTEGER`

**Possible Values**

* `10000`
* `0` (if no records were written)

---

## Column: `count_difference`

**Purpose**
The absolute difference between `source_extracted_count` and `target_loaded_count`. This helps detect dropped, duplicate, or corrupted records in transit.

**Data Type**
`INTEGER`

**Possible Values**

* `0` (exact match)
* `+5` (excess at target)
* `-10` (missing at target)

---

## Column: `count_difference_percent`

**Purpose**
The percentage difference between source and target counts, relative to the source extracted count. Helps normalize discrepancies across pipelines with varying volumes.

**Data Type**
`FLOAT`

**Possible Values**

* `0.0` (perfect match)
* `0.02` (2% drift)
* `-0.01` (1% shortfall)

---


## Column: `elt_process_status`

**Purpose**
Describes the technical execution status of the pipeline’s ELT (Extract, Load, Transform) phase. It tracks whether the data movement and transformations completed as expected.

**Data Type**
`STRING`

**Possible Values**

* `PENDING` — Execution not yet started
* `STARTED` — In progress
* `COMPLETED` — Finished successfully
* `FAILED` — Encountered an error
* `SKIPPED` — Step bypassed intentionally

---

## Column: `audit_process_status`

**Purpose**
Indicates the outcome of the audit step that validates data consistency, such as count checks or hash comparisons. It refers to whether audit logic was executed successfully, not whether the data matched.

**Data Type**
`STRING`

**Possible Values**

* `PENDING`
* `STARTED`
* `COMPLETED`
* `FAILED`
* `SKIPPED`

---

## Column: `audit_result_status`

**Purpose**
Captures the **result of the audit logic**. It conveys whether the data validated successfully (e.g., counts match), even if audit\_process\_status was technically successful.

**Data Type**
`STRING`

**Possible Values**

* `MATCHED` — Data validated correctly
* `MISMATCHED` — Audit completed but data did not match
* `NOT_VALID` — Audit was inconclusive or logically incorrect

---

## Column: `pipeline_final_status`

**Purpose**
Represents the **overall outcome** of the pipeline run. It is a summary field derived from ELT status, audit execution, and audit result. Useful for dashboards and monitoring views.

**Data Type**
`STRING`

**Possible Values**

* `PENDING`
* `STARTED`
* `COMPLETED`
* `FAILED`
* `SKIPPED`

---

## Column: `misc_info_json`

**Purpose**
Stores optional and flexible metadata in JSON format that supports debugging, traceability, ownership, or manual re-execution. This field acts as a developer aid and catch-all for non-tabular diagnostics.

Typical use cases include:

* Error tracebacks and exception messages
* Manual override parameters for reruns
* Pipeline ownership details
* Comments, tags, or runtime decisions

**Data Type**
`STRING` or `VARIANT` (depending on the storage engine; Snowflake recommends `VARIANT`)

**Possible Values**
A valid JSON object. For example:

```json
{
  "error_message": "COPY INTO failed due to file format mismatch",
  "pipeline_owner": "team_data_platform",
  "replay_params": {
    "source": "elasticsearch",
    "date_range": "2025-06-13T00:00Z to 2025-06-13T01:00Z"
  },
  "notes": "Retry using updated stage file format"
}
```

This field is **optional**, but extremely useful during debugging and post-mortem analysis.

---
