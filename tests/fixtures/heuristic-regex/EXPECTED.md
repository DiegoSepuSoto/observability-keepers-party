# Expected behavior: heuristic-regex

Applies to `obs-audit` and `obs-score`.

Inputs: a targeted text search finds a route and metric call, but no language-aware AST parser is available.

Expected results: cite file and line and label route and instrumentation conclusions `heuristic`; state that text search may miss indirect wrappers.

Non-goal: do not present search matches as verified behavior.
