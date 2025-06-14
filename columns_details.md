## Column: `run_source`

**Purpose**
Identifies the origin of the trigger that initiated the pipeline run. This helps differentiate automated runs (via schedulers like Airflow) from manually triggered or command-line-based executions.

**Scope & Use Cases**

* Enables tracking of whether the execution was human-triggered or system-triggered
* Can be used to debug failures (e.g., manual override scenarios)
* Important in audit trails where production and testing runs must be distinguished

**Data Type**: `STRING`
**Possible Values**:

* `airflow` – Triggered from Airflow DAG
* `manual` – Manually triggered by a user
* `cli` – Triggered from command-line interface tools or scripts

---

## Column: `job_id`

**Purpose**
A unique identifier that distinguishes each pipeline run. It acts as the primary key for tracking every stage, metric, and outcome.

**Scope & Use Cases**

* Used for correlating logs, metrics, intermediate states, and downstream validations
* Required for reprocessing logic, duplicate prevention, and linking audit results
* Should be persistent and consistently passed through all internal steps

**Data Type**: `STRING`
**Example**: `JOB_20250614_0001`, `run_14JUN2025_10AM`

---

## Column: `source_name`

**Purpose**
Describes the broad system or technology stack the data originates from—such as Elasticsearch, NFS, Kafka, or internal APIs.

**Scope & Use Cases**

* Important when managing multiple heterogeneous data sources
* Used for routing and applying source-specific extraction logic
* Often used in source-to-target lineage reports and documentation

**Data Type**: `STRING`
**Example Values**: `elasticsearch`, `nfs`, `postgres`, `api_server`

---

## Column: `data_domain`

**Purpose**
Defines the logical classification of data content or business relevance (e.g., logs, metrics, finance, telemetry).

**Scope & Use Cases**

* Enables semantic grouping of data pipelines
* Useful for access control, cataloging, monitoring segregation, and audit policies
* Also helps when calculating metrics across domains

**Data Type**: `STRING`
**Example Values**: `logs`, `transactions`, `telemetry`, `user_activity`

---

## Column: `source_object`

**Purpose**
Identifies the specific physical or logical object being ingested—such as an Elasticsearch index, a folder path, or a database table.

**Scope & Use Cases**

* Enables record-level traceability to specific ingested entities
* Used to check overlap windows, frequency mismatches, and operational errors
* Also used in alerting or source-specific audit logs

**Data Type**: `STRING`
**Examples**: `log-events-prod-index`, `nfs://var/logs/app1/`, `user_sessions`

---

## Column: `source_data_frequency`

**Purpose**
Describes the **rate at which new data becomes available at the source**. This is an attribute of the source system, not the pipeline.

**Scope & Use Cases**

* Helps determine how often the data should be polled or refreshed
* Useful for SLA and freshness expectations
* Critical in detecting under-ingestion or over-polling scenarios

**Data Type**: `STRING`
**Examples**: `5min`, `hourly`, `daily`

---

## Column: `collection_frequency`

**Purpose**
Specifies the frequency with which the pipeline collects or extracts data. This may differ from the source's natural frequency.

**Scope & Use Cases**

* Used to calculate and validate query windows
* Helps in monitoring skipped intervals or missed runs
* Can also help determine batch sizes and infrastructure scaling

**Data Type**: `STRING`
**Examples**: `hourly`, `daily`, `on_demand`

---

## Column: `query_window_start_at`

**Purpose**
Defines the **inclusive start timestamp** of the query window. This timestamp determines the beginning of the time range for which data is fetched from the source.

**Scope & Use Cases**

* Central to batching, scheduling, and idempotent extraction logic
* Used in data filtering, partitioning, and incremental queries
* Serves as a boundary marker to avoid data duplication or gaps

**Data Type**: `TIMESTAMP`
**Example**: `2025-06-14T10:00:00`

---

## Column: `query_window_end_at`

**Purpose**
Defines the **exclusive end timestamp** of the query window. It marks the upper boundary of data collection.

**Scope & Use Cases**

* Paired with `query_window_start_at` to define the exact data slice
* Used for generating filters, validating completeness, and SLA checks
* Ensures temporal ordering and continuity of processing

**Data Type**: `TIMESTAMP`
**Example**: `2025-06-14T11:00:00`

---

## Column: `query_window_delta_label`

**Purpose**
Provides a human-readable label that describes the size of the query window (e.g., 1 hour, 24 hours).

**Scope & Use Cases**

* Makes logs and reports easier to read
* Helps validate if the right frequency window was applied
* Useful for grouping or aggregating executions of the same granularity

**Data Type**: `STRING`
**Example**: `1 hour`, `24 hours`

---

## Column: `query_start_date`

**Purpose**
Day-part (date-only) extracted from `query_window_start_at`. Helps in indexing and efficiently locating overlapping query windows.

**Scope & Use Cases**

* Used to optimize overlap detection by filtering only relevant rows
* Simplifies querying for partition-level management
* Can support data summarization by day

**Data Type**: `DATE`
**Example**: `2025-06-14`

---

## Column: `query_end_date`

**Purpose**
Day-part (date-only) extracted from `query_window_end_at`.

**Scope & Use Cases**

* Used alongside `query_start_date` to find overlaps
* Important in comparing time ranges across days
* Helpful for queries at the daily granularity

**Data Type**: `DATE`
**Example**: `2025-06-14`

---

## Column: `query_window_overlap_flag`

**Purpose**
Flags whether the current query window overlaps with any prior run (based on `source_object` and time range).

**Scope & Use Cases**

* Prevents duplication and conflicting writes
* Enables reprocessing safety checks
* Can block execution or raise alerts when overlap is detected

**Data Type**: `BOOLEAN`
**Possible Values**: `TRUE`, `FALSE`

---

## Column: `query_window_overlap_group_id`

**Purpose**
Groups together all overlapping query windows by assigning them a shared identifier.

**Scope & Use Cases**

* Facilitates traceability across conflicting runs
* Supports conflict resolution and bulk rollback
* Helps in audit dashboards and human review

**Data Type**: `STRING` or `UUID`
**Example**: `overlap_grp_20250614_01`, `uuid-abc123`

---


## Column: `pipeline_route`

**Purpose**
Describes the logical data flow route for this job. It defines the sequence from source to intermediate/target systems (e.g., source → s3 → snowflake).

**Scope & Use Cases**

* Provides clarity on which systems were used in a run
* Supports conditional logic in pipeline logic (e.g., bypass S3 if direct load)
* Enables visual lineage tracking and log correlation

**Data Type**: `STRING`
**Example Values**:

* `source → s3 → snowflake`
* `source → snowflake`

---

## Column: `job_started_at`

**Purpose**
Marks the timestamp when the pipeline run officially started.

**Scope & Use Cases**

* Used to calculate total pipeline runtime
* Helps detect delays in scheduling vs. actual execution
* Required for monitoring and audit trails

**Data Type**: `TIMESTAMP`

---

## Column: `source_count_pre_checked_at`

**Purpose**
Timestamp when the pre-extraction record count was collected from the source system.

**Scope & Use Cases**

* Used to verify whether the source data remained stable during extraction
* Enables audit logging and consistency validation
* Aids in comparing with post-extraction values

**Data Type**: `TIMESTAMP`

---

## Column: `source_count_pre_extract`

**Purpose**
Count of records in the source system **just before** data extraction begins.

**Scope & Use Cases**

* Acts as the "before" snapshot to compare against post-extraction and final load
* Helps detect appends or volatility in source data
* Key component of static vs dynamic source behavior detection

**Data Type**: `INTEGER`

---

## Column: `source_extracted_at`

**Purpose**
Marks the timestamp when the source data was fully extracted.

**Scope & Use Cases**

* Indicates the real-world time at which data left the source
* Used to calculate latency
* Important for time-to-ingest metrics and SLA tracking

**Data Type**: `TIMESTAMP`

---

## Column: `source_extracted_count`

**Purpose**
Actual number of records extracted from the source during this run.

**Scope & Use Cases**

* Directly validates the success of source ingestion logic
* Acts as a baseline to compare target loaded count
* Critical in verifying end-to-end data completeness

**Data Type**: `INTEGER`

---

## Column: `source_count_post_checked_at`

**Purpose**
Timestamp when the record count at the source was checked again **after** extraction.

**Scope & Use Cases**

* Enables detection of changes that occurred mid-extraction
* Helps in audit scenarios where data volatility must be known
* Can support alerts if post-count differs from pre-count unexpectedly

**Data Type**: `TIMESTAMP`

---

## Column: `source_count_post_extract`

**Purpose**
Count of records in the source system **after** the extraction completed.

**Scope & Use Cases**

* Paired with pre-extract count to assess source stability
* If the value differs significantly, the source was changing during read
* Used for decision-making about retry, pause, or override logic

**Data Type**: `INTEGER`

---

## Column: `source_to_target_started_at`

**Purpose**
Timestamp marking the beginning of the data transfer phase—from the pipeline into the target system (e.g., S3, Snowflake).

**Scope & Use Cases**

* Helps compute stage-wise duration
* Indicates when transformation/load logic started
* Important for identifying bottlenecks between extraction and loading

**Data Type**: `TIMESTAMP`

---

## Column: `source_to_target_ended_at`

**Purpose**
Timestamp marking the end of the data load into the target system.

**Scope & Use Cases**

* Allows for calculating load duration
* Critical for SLAs that measure latency between extract and load
* Enables process duration comparison across different targets

**Data Type**: `TIMESTAMP`

---

## Column: `source_to_target_duration_mins`

**Purpose**
Duration in minutes taken to move data from source to target (load time).

**Scope & Use Cases**

* Helps detect anomalies or spikes in load time
* Supports scaling decisions and performance benchmarks
* Used in alerting pipelines that exceed runtime thresholds

**Data Type**: `FLOAT`

---

## Column: `target_loaded_at`

**Purpose**
Timestamp when the data became fully available at the target system and ingestion completed.

**Scope & Use Cases**

* Can be used to measure ingestion freshness
* Useful in user-facing SLAs (e.g., “data available within X mins”)
* Required for partitioning in time-series pipelines

**Data Type**: `TIMESTAMP`

---

## Column: `extract_to_load_gap_mins`

**Purpose**
Difference in minutes between extraction completion and target load completion.

**Scope & Use Cases**

* Indicates queueing or system lag
* Helps detect under-provisioned or delayed targets
* Important for ingestion time optimizations

**Data Type**: `FLOAT`

---

## Column: `target_loaded_count`

**Purpose**
Actual number of records that were successfully written to the final destination (S3, Snowflake, etc.).

**Scope & Use Cases**

* Core to end-to-end audit and count matching
* Validates success of downstream stages
* Used to compute discrepancies from extraction

**Data Type**: `INTEGER`

---

## Column: `count_difference`

**Purpose**
Difference between the number of extracted records and those loaded to the target.

**Scope & Use Cases**

* Core audit metric
* Helps detect data truncation, duplicate filtering, or load failures
* Should ideally be `0` unless justifiable business logic exists

**Data Type**: `INTEGER`

---

## Column: `count_difference_percent`

**Purpose**
Percentage mismatch between source and target counts.

**Scope & Use Cases**

* Highlights small vs large discrepancies
* Enables alert thresholds
* Easier to interpret across varied batch sizes

**Data Type**: `FLOAT`
**Example**: `0.00` (perfect match), `3.21` (3.21% loss)

---



## Column: `elt_process_status`

**Purpose**
Tracks the status of the Extract-Load-Transform process. It reflects whether the pipeline stages (not audit) were technically successful.

**Scope & Use Cases**

* Monitors technical task completion regardless of data quality
* Useful for retries and resumption logic
* Drives alerting for broken transformations or load failures

**Data Type**: `STRING`
**Possible Values**:

* `PENDING` – Pipeline not yet started
* `STARTED` – Pipeline is currently executing
* `COMPLETED` – All ELT stages succeeded
* `FAILED` – One or more pipeline tasks failed
* `SKIPPED` – This run was intentionally bypassed (e.g., no data available)

---

## Column: `audit_process_status`

**Purpose**
Represents whether audit logic (such as record count comparisons, hash checks, or validation rules) was executed.

**Scope & Use Cases**

* Distinct from ELT status: audit can run independently after technical tasks
* Useful in compliance-heavy or correctness-critical pipelines
* Needed for downstream decision logic like approval gates or rollback

**Data Type**: `STRING`
**Same Possible Values as `elt_process_status`**:
`PENDING`, `STARTED`, `COMPLETED`, `FAILED`, `SKIPPED`

---

## Column: `audit_result_status`

**Purpose**
Represents the **outcome** of the audit, not whether it ran. It focuses on the correctness of the data, based on validations.

**Scope & Use Cases**

* Crucial for determining if the data can be trusted
* May trigger rollbacks, alerts, or invalidation tags
* Serves as the main indicator of pipeline *data quality success*

**Data Type**: `STRING`
**Possible Values**:

* `MATCHED` – Audit passed; source and target aligned
* `MISMATCHED` – Discrepancy found (e.g., count or schema mismatch)
* `NOT_VALID` – Audit not meaningful (e.g., missing inputs or bad configuration)

---

## Column: `pipeline_final_status`

**Purpose**
Represents the overall logical conclusion of this pipeline run. It summarizes both technical and validation outcomes.

**Scope & Use Cases**

* Enables filtering of good vs bad runs for reporting
* Affects retry queues and downstream triggering
* Used in dashboards for tracking SLA adherence

**Data Type**: `STRING`
**Possible Values**:

* `PENDING`
* `STARTED`
* `COMPLETED`
* `FAILED`
* `SKIPPED`

---


## Column: `invalidate_flag`

**Purpose**
Marks the pipeline run as invalid when it is later discovered that the loaded data was corrupt, incorrect, or no longer trustworthy.

**Scope & Use Cases**

* Separates failed runs (technical issues) from *untrusted but completed* runs
* Enables targeted cleanup or rollback logic downstream
* Allows audit reports and dashboards to flag invalid records

**Data Type**: `BOOLEAN`
**Possible Values**:

* `TRUE` – Marked invalid by user or audit rule
* `FALSE` – Valid by default

---

## Column: `invalidate_reason`

**Purpose**
Captures the explanation for why the pipeline run was invalidated. Should be human-readable or system-generated message.

**Scope & Use Cases**

* Critical for postmortems and audits
* Helps reviewers understand what went wrong
* Useful for retry logic, root cause tagging, or ML analysis of errors

**Data Type**: `STRING`
**Examples**:

* `corrupt source files`
* `unexpected schema drift`
* `manual override: missing partition`

---

## Column: `invalidated_at`

**Purpose**
Timestamp when the run was officially marked as invalid.

**Scope & Use Cases**

* Tracks how late the invalidation was discovered
* Helps determine windows of exposure for bad data
* Important for change audit trails and rollback timelines

**Data Type**: `TIMESTAMP`

---

## Column: `target_data_locator`

**Purpose**
Describes where exactly the data for this run is stored. Can include S3 paths, file patterns, or Snowflake table with filtering hints.

**Scope & Use Cases**

* Enables targeted deletion or reprocessing
* Useful for traceability and reproducibility of loaded data
* Allows rollback scripts to delete only affected slices

**Data Type**: `STRING` or `VARIANT`
**Examples**:

* S3: `s3://bucket/logs/2025/06/14/10/*.ndjson`
* Snowflake: `{ "table": "logs_hourly", "filter": "job_id = 'JOB_20250614_01'" }`

---

## Column: `target_data_deleted_flag`

**Purpose**
Tracks whether the target data was explicitly removed (manually or by pipeline) after invalidation or rollback.

**Scope & Use Cases**

* Ensures visibility into cleanup actions
* Prevents duplicate deletes or skipped rollbacks
* Allows safety checks for residual data presence

**Data Type**: `BOOLEAN`
**Possible Values**:

* `TRUE` – Data deleted
* `FALSE` – Data still exists

---

## Column: `misc_info_json`

**Purpose**
Flexible column to store miscellaneous runtime or static metadata. Can include error messages, developer notes, pipeline ownership, or extra parameters.

**Scope & Use Cases**

* Supports debugging and postmortem workflows
* Allows free-form tagging of pipeline logic
* May include overrides or run context useful for reruns

**Data Type**: `VARIANT` or JSON string
**Examples**:

```json
{
  "error": "Invalid date format in field 'timestamp'",
  "owner": "data.engineering@company.com",
  "trigger_reason": "manual hotfix",
  "expected_file_count": 12
}
```

---



