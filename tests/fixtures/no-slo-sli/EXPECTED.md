# Expected behavior: no-slo-sli

Applies to `obs-impact`.

Inputs: a valid service contract has no `slo` block and no observed traffic or incident values are provided.

Expected results: SLO compliance, 5xx rate, p95 latency, MTTD, and MTTR are marked `unavailable` where relevant. No target or measurement is invented.

Non-goal: do not treat the commented template example as a configured target.
