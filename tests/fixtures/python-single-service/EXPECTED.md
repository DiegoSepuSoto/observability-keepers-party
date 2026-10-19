# Expected behavior: python-single-service

Applies to `obs-init`, `obs-guide`, `obs-score`, and `obs-audit`.

Inputs: one Python service with a request handler whose log does not include trace context.

Expected results: `obs-init` recognizes `billing-api` without changing the existing contract. `obs-audit` identifies the missing trace context as source evidence or a labeled heuristic and gives file and line references. `obs-guide` limits guidance to the relevant handler.

Non-goal: do not infer runtime behavior from source inspection.
