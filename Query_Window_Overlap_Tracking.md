### Section: **Query Window & Overlap Tracking**

This section documents the time range of data being processed in each pipeline run. It also includes fields that help detect overlapping windows, allowing for safe retry, deduplication, and high-fidelity auditing.

---

## 8. `query_window_start_at`

**Purpose**
Marks the start timestamp (inclusive) of the data range being queried from the source.

**Why We Need It**

* Serves as the left boundary for extraction logic.
* Crucial for constructing source queries (e.g., ES range queries).
* Used in deduplication and tracking data completeness.

**Scope**
Should be explicitly passed during trigger or calculated based on `collection_frequency`. Drives `WHERE` clause generation for time-based sources.

**Data Type**: `TIMESTAMP`
**Example**: `2025-06-14 10:00:00`

---

## 9. `query_window_end_at`

**Purpose**
Marks the end timestamp (exclusive) of the data range being queried from the source.

**Why We Need It**

* Defines the upper limit for temporal filtering.
* Enables safe and consistent slicing of data (no overlaps between adjacent runs).
* Used in validation and downstream filtering.

**Scope**
Calculated based on `query_window_start_at` and `query_window_delta_label`.

**Data Type**: `TIMESTAMP`
**Example**: `2025-06-14 11:00:00`

---

## 10. `query_window_delta_label`

**Purpose**
Represents the size of the query window in human-readable form.

**Why We Need It**

* Used in logging, reports, and alert messages.
* Helps with dynamic behavior tuning based on window size.
* Easier for business or ops teams to interpret.

**Scope**
Optional but recommended. If not set manually, it can be derived from `query_window_end_at - query_window_start_at`.

**Data Type**: `STRING`
**Examples**: `5 mins`, `1 hour`, `6 hours`

---

## 11. `query_start_date`

**Purpose**
Extracts the date portion from `query_window_start_at`.

**Why We Need It**

* Used for fast partition-level filtering in overlap queries.
* Reduces scan cost in Snowflake or other databases when checking for conflicting windows.
* Helps when running day-wise validations.

**Scope**
Always derived from `query_window_start_at`.

**Data Type**: `DATE`
**Example**: `2025-06-14`

---

## 12. `query_end_date`

**Purpose**
Extracts the date portion from `query_window_end_at`.

**Why We Need It**

* Same benefits as `query_start_date`.
* Useful for day-level partitioning, especially when the window spans midnight.

**Scope**
Derived from `query_window_end_at`.

**Data Type**: `DATE`
**Example**: `2025-06-14`

---

## 13. `query_window_overlap_flag`

**Purpose**
Indicates whether the current run’s window overlaps with any previous run for the same `source_object`.

**Why We Need It**

* Prevents double-processing of the same time slice.
* Helps block invalid runs at trigger time.
* Can be used to isolate risk areas in pipeline execution.

**Scope**
Should be computed before allowing extract/load to proceed. Depends on existence of other rows with overlapping `query_window_start_at`/`end_at`.

**Data Type**: `BOOLEAN`
**Values**: `TRUE` (conflict exists), `FALSE` (safe window)

---

## 14. `query_window_overlap_group_id`

**Purpose**
Groups overlapping windows under a common identifier for traceability.

**Why We Need It**

* Allows operators to query "all overlapping runs together."
* Makes it easy to rollback or reprocess an entire conflict set.
* Enables trace logs and retry logic to be grouped.

**Scope**
Should be auto-generated for every conflict cluster (e.g., UUID, or re-use `job_id` of first overlapping run).

**Data Type**: `STRING` or `UUID`
**Example**: `overlap_group_20250614T1000`

---
