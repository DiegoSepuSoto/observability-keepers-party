# Expected behavior: async-context-propagation

Applies to `obs-audit` and `obs-guide`.

Inputs: a message producer injects W3C context into headers and a consumer extracts `traceparent` before processing.

Expected results: source evidence is reported with file and line. AST evidence may be verified; targeted text search is labeled heuristic. The skills do not infer runtime propagation from this fixture.

Non-goal: do not claim delivery or context continuity at runtime.
