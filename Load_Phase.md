### Section: **Load Phase (Source to Target Tracking)**

This section captures metadata about the loading of data into the target system (e.g., Snowflake). It measures the duration of transfer, records timestamps, counts, and derives metrics for performance monitoring and auditability.

---

## 22. `source_to_target_started_at`

**Purpose**
Timestamp when the transfer of extracted data into the target system began.

**Why We Need It**

* Defines the beginning of the load phase.
* Key timestamp for monitoring latency from extraction to delivery.
* Supports tracking time gaps between pipeline phases.

**Scope**
Logged immediately before initiating the target load operation (e.g., Snowflake COPY INTO).

**Data Type**: `TIMESTAMP`

---

## 23. `source_to_target_ended_at`

**Purpose**
Timestamp when loading data into the target was completed.

**Why We Need It**

* Complements `source_to_target_started_at` to measure duration.
* Used in freshness monitoring and detecting stuck loads.
* Important for end-to-end data availability checks.

**Scope**
Should be logged only after verifying the target system acknowledges full load (e.g., COPY INTO status = `LOADED`).

**Data Type**: `TIMESTAMP`

---

## 24. `source_to_target_duration_mins`

**Purpose**
Actual number of minutes it took to transfer data from source (post-extraction) to the target system.

**Why We Need It**

* Core operational metric for system performance.
* Detects bottlenecks in file upload, staging, or SQL execution.
* Useful for warehouse sizing and alerting.

**Scope**
Should be calculated as:

```sql
TIMESTAMPDIFF(MINUTE, source_to_target_started_at, source_to_target_ended_at)
```

**Data Type**: `FLOAT`

---

## 25. `target_loaded_at`

**Purpose**
Timestamp when the data was fully available and committed in the target system.

**Why We Need It**

* Provides a single final point-in-time reference for data availability.
* Used by downstream consumers for freshness validation.
* Helps schedule downstream ETL or model refreshes.

**Scope**
Should reflect the actual completion of all write operations—not just initiation.

**Data Type**: `TIMESTAMP`

---

## 26. `extract_to_load_gap_mins`

**Purpose**
Gap in minutes between `source_extracted_at` and `target_loaded_at`.

**Why We Need It**

* Measures latency between pipeline phases.
* Detects pipeline delays and integration slowness.
* Can help in SLA alerting and root cause diagnosis.

**Scope**
Derived as:

```sql
TIMESTAMPDIFF(MINUTE, source_extracted_at, target_loaded_at)
```

**Data Type**: `FLOAT`

---

## 27. `target_loaded_count`

**Purpose**
Total number of records successfully written and committed into the target (e.g., Snowflake table).

**Why We Need It**

* Primary metric for auditing accuracy.
* Compared against `source_extracted_count` to detect data loss or duplication.
* Useful for verifying correctness after COPY INTO or ingestion scripts.

**Scope**
Should be derived from Snowflake metadata or audit logs immediately post-load.

**Data Type**: `INTEGER`

---

## 28. `count_difference`

**Purpose**
Difference in record count between extraction and loading phases.
Computed as:

```sql
target_loaded_count - source_extracted_count
```

**Why We Need It**

* Direct indicator of data movement accuracy.
* Zero means perfect match; any deviation needs investigation.
* Enables threshold-based validations.

**Scope**
Used in audit reports, anomaly detection, retry triggers.

**Data Type**: `INTEGER`

---

## 29. `count_difference_percent`

**Purpose**
Percentage error in count comparison between extracted and loaded records.

**Why We Need It**

* Normalizes `count_difference` across large/small loads.
* Helps define tolerance policies (e.g., allow ±0.5%).
* Essential for alerts and SLAs.

**Scope**
Formula:

```sql
ABS(count_difference) * 100.0 / NULLIF(source_extracted_count, 0)
```

**Data Type**: `FLOAT`

---
