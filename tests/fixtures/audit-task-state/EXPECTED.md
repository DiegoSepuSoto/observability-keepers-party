# Expected behavior: audit-task-state

Applies to `obs-audit`.

Inputs: one open propagation task with category and scope matching the finding, plus a done task with the highest sequence number `009`.

Expected results: `obs-audit` does not create a duplicate for the open task and mentions the skipped duplicate. A different selected finding receives ID `010`, counting the done task when choosing the next sequence.

Non-goal: do not overwrite or renumber existing tasks.
