## Revised Requirement Specification: Execution Selector Script

**Purpose**
To filter and return the list of valid `PENDING` records from the `pipeline_lifecycle` table that are eligible for execution. The script only performs **record selection** based on well-defined retry and window ordering logic. It does **not execute** the pipeline or perform any row updates.

---

### Functional Objective

Identify candidate records from the `pipeline_lifecycle` table where:

* The record is still pending (`elt_process_status = 'PENDING'`)
* It represents the most recent retry attempt for a specific query window
* The list is sorted in correct execution order for downstream processing

---

### Input Parameters (Optional)

To narrow down the result set, the following inputs may be provided:

* `source_object` (string)
* `data_domain` (string)
* `execution_date` (date or range)
* Any other scoping filter (e.g., domain tag, pipeline priority class)

---

### Selection Logic

1. **Filter**:
   Select all records where:

   * `elt_process_status = 'PENDING'`

2. **Group & Reduce**:
   For each unique combination of:

   * `source_object`
   * `query_window_start_at`
     Keep only the row with the **maximum `retry_attempt`**

3. **Sort**:
   Order the filtered results by:

   * `retry_attempt DESC`
   * `query_window_start_at ASC`

   This ensures:

   * Retries are handled before first-time runs
   * Within the same retry level, windows are processed in chronological order

---

### Output

* A list (or iterable) of candidate records to be passed to downstream handlers
* Each record is guaranteed to:

  * Be in `PENDING` state
  * Be the highest retry attempt for its query window
  * Be in correct priority order for execution

---

### What This Script Does *Not* Do

* It does **not** execute any pipeline run
* It does **not** update statuses (e.g., `STARTED`, `COMPLETED`, `FAILED`)
* It does **not** assign or modify `job_id`
* It does **not** insert retry rows

