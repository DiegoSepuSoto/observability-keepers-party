# Expected behavior: investigate-unconfirmed-signal

Applies to `obs-investigate`.

Inputs: the symptom "p95 latency on `POST /checkout` rose 40% at 14:00 UTC" with `metric_samples.csv`, where p95 stays between 405 and 418 ms across all windows.

Expected results: the skill reports the change as unconfirmed noise in Step 1, cites the sampled values, and stops without proposing a dimension search or a confirmed finding.

Non-goal: do not recommend application source changes or scan repository source.
