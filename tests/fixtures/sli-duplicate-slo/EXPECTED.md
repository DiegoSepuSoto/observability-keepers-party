# Expected behavior: sli-duplicate-slo

Applies to `obs-sli` and `obs-audit`.

Inputs: a config whose `slo` list already covers `POST /checkout` availability; the user asks `obs-sli` for a checkout availability SLI.

Expected results: `obs-sli` reports the existing SLO and stops instead of generating a duplicate. `obs-audit` finds this event-based SLI acceptable and creates no `sli` task.

Non-goal: do not invent a target or modify the existing entry.
