# Expected behavior: no-critical-routes

Applies to `obs-score`.

Inputs: the service contract has no `critical_routes` list and source contains no externally reachable HTTP, RPC, or GraphQL handler.

Expected results: traces, metrics, and logs all report `unknown` because no valid denominator exists. No route is invented from library functions.

Non-goal: do not report zero percent as if a route denominator existed.
