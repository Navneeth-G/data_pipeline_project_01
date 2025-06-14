### Section: **Run Identification & Source Metadata**

This section defines how each pipeline run is uniquely identified, what data domain it belongs to, where the data originates, and what the expected data frequency characteristics are. These columns form the metadata backbone of the pipeline and guide the rest of the flow.

---

## 1. `run_source`

**Purpose**
Identifies how the pipeline was triggered—whether by Airflow, manual execution, CLI test, or an external system.

**Why We Need It**

* Useful for audit trails: distinguishes automated vs ad hoc runs.
* Enables special-case logic: for example, stricter validation for automated runs.
* Helps explain failures due to environment differences (e.g., permission mismatch in manual runs).

**Scope**
Applies across all pipeline types. The value should be passed explicitly as part of the pipeline trigger mechanism (e.g., Airflow variables or CLI arguments).

**Data Type**: `STRING`
**Expected Values**:

* `airflow` – Run triggered by Airflow DAG
* `manual` – Run manually by a user (e.g., in Python REPL or notebook)
* `cli` – Run via CLI tooling
* `other` – Any other orchestration method (e.g., cloud event)

---

## 2. `job_id`

**Purpose**
Serves as a unique identifier for every execution of the pipeline lifecycle.

**Why We Need It**

* Enables full traceability across logs, files, and database records.
* Allows audit and retry logic to pinpoint a single run.
* All downstream processing, rollback, or cleanup must reference `job_id`.

**Scope**
Should be generated consistently at the beginning of each pipeline run. Typically a concatenation of pipeline name, timestamp, and a run token (e.g., `PIPELINE_X_20250614T1000Z`).

**Data Type**: `STRING`

---

## 3. `source_name`

**Purpose**
Identifies the source system or platform where the data originates.

**Why We Need It**

* Enables source-specific logic in extractors.
* Required to configure connector behavior (e.g., ES, NFS, API).
* Helps organize lineage and observability.

**Scope**
This field should match your internal source registry (if any). All upstream logic branches based on `source_name`.

**Data Type**: `STRING`
**Examples**:

* `elasticsearch_logs`
* `k8s_nfs_mount`
* `external_api`

---

## 4. `data_domain`

**Purpose**
Represents the logical domain the data belongs to—e.g., telemetry, logs, product events.

**Why We Need It**

* Enables grouping of pipelines by business context.
* Supports modular design, access policies, and ownership models.
* Important for organizing monitoring dashboards and retry queues.

**Scope**
Assigned manually or mapped from `source_name`. Enables coarse-grain control and reporting.

**Data Type**: `STRING`
**Examples**:

* `application_logs`, `security_events`, `financial_transactions`

---

## 5. `source_object`

**Purpose**
Specifies the exact entity or unit of data extraction inside the source—typically an index name, file path pattern, table, or endpoint.

**Why We Need It**

* Determines what to pull in each run.
* Required for query logic and deduplication.
* Used in overlap detection and schema versioning.

**Scope**
Populated by operator or metadata loader. Often varies within the same `source_name`.

**Data Type**: `STRING`
**Examples**:

* `access-logs-2025-06`, `/mnt/logs/*.json`, `prod_event_stream`

---

## 6. `source_data_frequency`

**Purpose**
Indicates how often data is produced at the source system.

**Why We Need It**

* Aligns pipeline granularity to data availability.
* Prevents over-fetching or under-fetching.
* Useful for anomaly detection (e.g., source not producing as expected).

**Scope**
Configured statically per pipeline or inferred dynamically. This is a business-level frequency—not the actual pipeline schedule.

**Data Type**: `STRING`
**Examples**:

* `5 mins`, `hourly`, `daily`, `continuous`

---

## 7. `collection_frequency`

**Purpose**
Specifies how often the pipeline attempts to collect data from the source.

**Why We Need It**

* Helps verify scheduling alignment with source cadence.
* Can be compared against `source_data_frequency` to detect misconfigurations.
* Useful for SLA enforcement and gap analysis.

**Scope**
This is the *intended* collection frequency. It may be configured in Airflow or in code parameters.

**Data Type**: `STRING`
**Examples**:

* `5 mins`, `hourly`, `manual`, `adhoc`

---

