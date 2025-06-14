
#### 1. Run and Source Metadata

1. `run_source`
2. `job_id`
3. `source_name`
4. `data_domain`
5. `source_object`
6. `source_data_frequency`
7. `collection_frequency`

#### 2. Query Window and Overlap

8. `query_window_start_at`
9. `query_window_end_at`
10. `query_window_delta_label`
11. `query_start_date`
12. `query_end_date`
13. `query_window_overlap_flag`
14. `query_window_overlap_group_id`

#### 3. Extraction Tracking

15. `job_started_at`
16. `source_count_pre_checked_at`
17. `source_count_pre_extract`
18. `source_extracted_at`
19. `source_extracted_count`
20. `source_count_post_checked_at`
21. `source_count_post_extract`

#### 4. Load Phase: Source to Target

22. `source_to_target_started_at`
23. `source_to_target_ended_at`
24. `source_to_target_duration_mins`
25. `target_loaded_at`
26. `extract_to_load_gap_mins`
27. `target_loaded_count`
28. `count_difference`
29. `count_difference_percent`

#### 5. ELT and Audit Process Status

30. `elt_process_status`
31. `audit_process_status`
32. `audit_result_status`
33. `pipeline_final_status`

#### 6. Duration Expectations and Monitoring

34. `expected_extraction_duration_mins`
35. `actual_extraction_duration_mins`
36. `expected_load_duration_mins`
37. `actual_load_duration_mins`
38. `expected_audit_duration_mins`
39. `actual_audit_duration_mins`
40. `expected_pipeline_duration_mins`
41. `actual_pipeline_duration_mins`

#### 7. Invalidation & Recovery Tracking

42. `is_invalidated_flag`
43. `is_replacement_run_flag`
44. `target_deletion_done_flag`

#### 8. Target Traceability & Metadata

45. `target_trace_info`
46. `record_inserted_at`
47. `record_last_updated_at`
48. `misc_info_json`

