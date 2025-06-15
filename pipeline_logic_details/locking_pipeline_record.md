**Purpose**
To transition a single `PENDING` pipeline lifecycle record into `STARTED` state, establishing exclusive ownership of that run. This script ensures that only one execution agent (e.g., DAG, CLI, scheduler) is authorized to process that specific job, preventing duplicates or concurrency conflicts.

---

### Functional Behavior

* Accepts a single `PENDING` record from the `pipeline_lifecycle` table
* Performs the following atomic updates:

  * Sets `elt_process_status = 'STARTED'`
  * Assigns a new unique `job_id` if not already set
  * Updates `record_last_updated_at = current_timestamp`
* Returns the updated record for downstream ELT processing

---

### Input

* One `PENDING` record (or a unique identifier to fetch it), including:

  * `source_object`
  * `query_window_start_at`
  * `retry_attempt`

---

### Output

* Updated record from `pipeline_lifecycle`, marked as:

  * `elt_process_status = 'STARTED'`
  * Assigned `job_id`
  * Timestamped for lifecycle traceability

---

### Notes

* This script must be invoked **before** any source count, extract, or load actions
* It should be used in coordination with the **Execution Selector Script**
* Designed to handle **exactly one record** per call, ensuring job-level atomicity

---
