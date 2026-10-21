# Expected behavior: critical-routes-configured

Applies to `obs-score`.

Inputs: the contract explicitly declares one critical route even though source discovery could find additional handlers.

Expected results: the declared route takes precedence, is the denominator for traces, metrics, and logs, and is cited as `config` evidence with a config line.

Non-goal: do not add inferred routes to the configured denominator.
