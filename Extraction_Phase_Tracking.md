### Section: **Extraction Phase Tracking**

This section tracks how and when data was pulled from the source system. It includes metadata about pre/post checks, extraction timestamp, and counts. These columns are critical for debugging volatility, retry behavior, and detecting issues like partial reads or source churn.

---

## 15. `job_started_at`

**Purpose**
Marks the official start timestamp of the pipeline run, immediately before any extraction begins.

**Why We Need It**

* Reference point for all duration calculations.
* Enables freshness and delay analysis.
* Useful for dashboards, run ordering, and latency tracking.

**Scope**
Should be logged as the very first action of the run. All duration fields are measured from this point.

**Data Type**: `TIMESTAMP`

---

## 16. `source_count_pre_checked_at`

**Purpose**
Timestamp when a count was performed on the source data **before** extraction began.

**Why We Need It**

* Provides a baseline to compare with post-extract source state.
* Detects volatility in sources (e.g., logs still being written).
* Enables confidence scoring for source consistency.

**Scope**
Should be triggered as close as possible to the start of extract, using the same filter window.

**Data Type**: `TIMESTAMP`

---

## 17. `source_count_pre_extract`

**Purpose**
The count of records available at the source before extraction.

**Why We Need It**

* Used to compare with post-extract count and extract count.
* Key to understanding if source is static or dynamic.
* Helps explain downstream mismatches.

**Scope**
Captured from the same exact query as the one used for extraction—just with a `count` or `size` aggregation.

**Data Type**: `INTEGER`

---

## 18. `source_extracted_at`

**Purpose**
Timestamp marking when the source extraction finished or was committed.

**Why We Need It**

* Enables calculation of `actual_extraction_duration_mins`.
* Acts as handoff point between extract and load phases.
* Useful for lag diagnostics.

**Scope**
Should be recorded right after all source data is saved to intermediate buffer (e.g., S3, memory, disk).

**Data Type**: `TIMESTAMP`

---

## 19. `source_extracted_count`

**Purpose**
Number of records actually pulled from the source.

**Why We Need It**

* Core audit metric: how much we *actually* ingested.
* Compared against pre/post counts to evaluate stability.
* Used in retry logic to detect under-fetching or stalling.

**Scope**
Collected after the extraction script/process completes. This is the literal row count captured for the given window.

**Data Type**: `INTEGER`

---

## 20. `source_count_post_checked_at`

**Purpose**
Timestamp of a second count performed after extraction completed.

**Why We Need It**

* Helps determine if the source changed *during or after* extraction.
* Critical for streaming-to-batch edge cases and volatile sources.

**Scope**
Run immediately after extract using the same query. Any mismatch with `pre_extract` suggests instability.

**Data Type**: `TIMESTAMP`

---

## 21. `source_count_post_extract`

**Purpose**
Count of records in the source after the extraction step.

**Why We Need It**

* Compared with pre-extract count to detect churn.
* Important for audit scoring and retry strategy.
* Key indicator for time-window correctness.

**Scope**
Same query conditions as `source_count_pre_extract`, taken after extract completes.

**Data Type**: `INTEGER`

---
