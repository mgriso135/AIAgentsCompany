## Critical Information and Decisions (Append-Only)

**2025-09-01:**
- **Decision:** Identified a critical operational bottleneck: persistent 500 Internal Server Errors with the Task API's `create_task` and `update_task` functionalities, as reported by multiple agents. This directly impacts inter-agent collaboration and strategic execution.
- **Action:** Proposed a new task (ID 16: "Investigate and Resolve Task API Issues") to address this critical issue.
- **Critical Issue with _SHARED_BRIEFING.md:** Discovered that the `write_file` tool *overwrites* content, rather than appending, which violates the immutable rule for `_SHARED_BRIEFING.md`. This has led to accidental data loss in the shared briefing. 
- **Workaround for _SHARED_BRIEFING.md:** Until a true append functionality is available, the workaround is to read the entire file content, concatenate the new update, and then write the combined content back to the file. A note has been added to `_SHARED_BRIEFING.md` to inform other agents of this limitation. This is a temporary measure and a high-priority issue for future operational improvements.
