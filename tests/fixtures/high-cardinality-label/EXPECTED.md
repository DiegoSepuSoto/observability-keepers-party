# Expected behavior: high-cardinality-label

Applies to `obs-guide`, `obs-audit`, and `obs-score`.

Inputs: one metric uses the built-in floor label `user_id`; another uses project-configured `tenant_code`, which is absent from the built-in floor.

Expected results: all three skills treat both labels as forbidden by applying the union of the built-in floor and `guardrails.forbidden_metric_labels`.

Non-goal: do not apply metric-label restrictions to `obs-init` or `obs-impact`.
