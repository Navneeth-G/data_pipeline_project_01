
### Requirement Specification: Daily Lifecycle Window Planner Script

**Objective:**
In order to support and operationalize the `pipeline_lifecycle` metadata layer in our data pipeline project, we need a standalone script that pre-generates and inserts all required pipeline run records for a given day into the `pipeline_lifecycle` table. This script acts as the **daily planner** and ensures that all query windows for all pipeline sources are scheduled in advance, enabling precise execution tracking, auditability, and retry alignment.

---

### Function Purpose

This script is responsible for pre-populating one row per query window per source into the `pipeline_lifecycle` table, using metadata configurations defined in centralized YAML files. It guarantees **no duplication**, **no cross-day spillover**, and supports **gap filling for partial days**.

---

### Functional Behavior

1. **Target Day Definition**

   * The script must accept a `target_date` (format: `YYYY-MM-DD`) to indicate for which day the lifecycle table needs to be populated.

2. **Configuration Loading**

   * Reads source-wise pipeline configuration from one or more YAML files. These include:

     * `source_name`, `source_object`, `data_domain`
     * `query_window_delta_label` (e.g., `1 hour`)
     * `collection_frequency`, `source_data_frequency`
     * `expected_*_duration_mins`
     * Any other static metadata required for insertion

3. **Query Window Generation**

   * For each source defined in the config:

     * Divide the 24-hour `target_date` into query windows based on `query_window_delta_label`
     * Each generated window must be represented by:

       * `query_window_start_at`: falls strictly within the `target_date`
       * `query_window_end_at`: exclusive end time (may extend into the next day)

4. **Idempotent Row Insertion**

   * For each `(source_object, query_window_start_at)` combination:

     * Check if the row already exists in `pipeline_lifecycle`
     * If it does not exist → insert the row
     * If it exists → skip
   * This ensures that repeated runs of the script do not duplicate data

5. **Gap Recovery**

   * If only partial records exist (e.g., due to failure or manual deletion), the script should **identify and insert only the missing windows**, restoring completeness for that day

6. **Column Defaults for Inserted Rows**

   * `job_id`: `NULL`
   * `elt_process_status`: `'PENDING'`
   * `audit_process_status`: `'PENDING'`
   * `audit_result_status`: `NULL`
   * `pipeline_final_status`: `'PENDING'`
   * `is_invalidated_flag`, `is_replacement_run_flag`, `target_deletion_done_flag`: `FALSE`
   * `record_inserted_at`, `record_last_updated_at`: current timestamp

7. **Boundary Enforcement**

   * The script must **only plan windows whose `query_window_start_at` falls within the `target_date`**
   * The `query_window_end_at` of the last window may reach `00:00:00` of the next day, but the window is **still part of the `target_date` batch**

8. **Optional Enhancements**

   * `dry_run` mode to preview insert actions without committing
   * Logging: number of total expected, already existing, and newly inserted rows
   * Error reporting if config is incomplete for any source


