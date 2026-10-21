# Expected behavior: missing-pillars

Applies to `obs-audit` and `obs-score`.

Inputs: one externally reachable route has no source evidence of a server span, a relevant counter or histogram, or a structured log with trace context.

Expected results: the route remains in one shared denominator for all three pillars; each uncovered pillar is reported as missing source evidence. Any audit output creates no more than two prioritized tasks.

Non-goal: do not convert missing source evidence into a runtime claim.
