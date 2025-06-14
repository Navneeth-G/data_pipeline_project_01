### Section: **Duration Expectations and Monitoring**

This section tracks both expected and actual durations for each pipeline stage. These fields support SLA enforcement, anomaly detection, resource allocation, and performance tuning.

---

## 34. `expected_extraction_duration_mins`

**Purpose**
Represents the target duration (in minutes) that extraction from the source should take under normal conditions.

**Why We Need It**

* Defines the SLA or operational expectation for extraction latency.
* Supports alerting if extraction exceeds expected time.
* Enables performance benchmarking across pipelines.

**Scope**
Configured statically per pipeline or derived from historical averages.

**Data Type**: `FLOAT` (minutes)

---

## 35. `actual_extraction_duration_mins`

**Purpose**
Actual time taken (in minutes) to extract data from the source during this run.

**Why We Need It**

* Enables runtime anomaly detection if extraction lags.
* Used to compare against `expected_extraction_duration_mins` for performance deviation.
* Required for post-mortems and pipeline optimization.

**Scope**
Derived as:

```sql
TIMESTAMPDIFF(MINUTE, job_started_at, source_extracted_at)
```

**Data Type**: `FLOAT`

---

## 36. `expected_load_duration_mins`

**Purpose**
Configured SLA or expected time to load data into the target system.

**Why We Need It**

* Helps detect bottlenecks in file upload or COPY INTO.
* Assists in warehouse size tuning and cost analysis.
* Can inform capacity planning and schedule gaps.

**Scope**
Configured based on load size, pipeline type, and system.

**Data Type**: `FLOAT`

---

## 37. `actual_load_duration_mins`

**Purpose**
Real time taken to complete the load from staging area to target.

**Why We Need It**

* Detects delays or system errors in writing to targets.
* Compares against `expected_load_duration_mins` for drift.
* Useful for investigating runtime slowness.

**Scope**
Derived as:

```sql
TIMESTAMPDIFF(MINUTE, source_to_target_started_at, source_to_target_ended_at)
```

**Data Type**: `FLOAT`

---

## 38. `expected_audit_duration_mins`

**Purpose**
Expected or budgeted duration of audit checks.

**Why We Need It**

* Helps detect audit stuck runs or timeouts.
* Enables alerting and SLA management for audit phase.

**Scope**
Configured based on volume, logic complexity, and audit types.

**Data Type**: `FLOAT`

---

## 39. `actual_audit_duration_mins`

**Purpose**
Time taken in the current run to perform all audit operations.

**Why We Need It**

* Enables audit performance tuning.
* Flags inefficiencies or resource starvation during auditing.
* Supports debugging of prolonged pipeline tail latency.

**Scope**
Derived from internal audit start/end times.

**Data Type**: `FLOAT`

---

## 40. `expected_pipeline_duration_mins`

**Purpose**
Expected total time for the entire pipeline run to complete from start to finish.

**Why We Need It**

* Enables global SLA compliance tracking.
* Serves as a performance benchmark across pipelines or clients.

**Scope**
Usually based on system capacity, data size, and business priority.

**Data Type**: `FLOAT`

---

## 41. `actual_pipeline_duration_mins`

**Purpose**
The real end-to-end duration of the full run.

**Why We Need It**

* Critical KPI for engineering and business stakeholders.
* Directly compared with `expected_pipeline_duration_mins` for efficiency.
* Useful for billing, capacity models, and throughput metrics.

**Scope**
Calculated as:

```sql
TIMESTAMPDIFF(MINUTE, job_started_at, target_loaded_at)
```

**Data Type**: `FLOAT`

---

