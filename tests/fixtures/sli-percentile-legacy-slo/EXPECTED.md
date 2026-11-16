# Expected behavior: sli-percentile-legacy-slo

Applies to `obs-audit` and `obs-sli`.

Inputs: a config using the legacy mapping-form `slo` block with a percentile latency target.

Expected results: `obs-audit` flags `p95_latency_target_ms` as not event-based and the block as legacy, and creates at most one task with category `sli`. `obs-sli` asks the user to migrate the block to the list format before appending a new entry.

Non-goal: do not treat a percentile aggregate as an acceptable SLI.
