# Expected behavior: indirect-wrapper

Applies to `obs-audit` and `obs-score`.

Inputs: a route invokes a project wrapper that creates a span indirectly.

Expected results: inspect the wrapper when relevant source is available. A targeted search that cannot resolve the wrapper remains heuristic and explicitly notes that indirect wrappers may be missed; do not claim certainty from a missing direct API call.

Non-goal: do not equate absence of a direct SDK call with absence of instrumentation.
