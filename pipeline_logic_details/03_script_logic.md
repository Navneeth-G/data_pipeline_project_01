## Requirement Specification: ELT + Audit Trigger Script

**Purpose**
To act as an execution bridge that takes selected `PENDING` records and forwards them to a downstream function responsible for performing the full ELT and audit lifecycle.

---

### Description

This script:

* Accepts as input: a list of valid `PENDING` records (from the execution selector)
* **Does not execute ELT or audit logic itself**
* For each record:

  * Passes it to a centralized handler function/module that performs:

    * Extraction
    * Loading
    * Auditing
    * Status updates and metrics logging

---

### Role in System

* Delegates full execution to specialized modules
* Keeps orchestration and logic separation clean
* Allows future scaling or branching without changing this script


