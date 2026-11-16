# Expected behavior: volume-dynamic-and-variable-labels

Applies to `obs-volume`.

Inputs: one counter mixes a stable route template and status class, a variable region, and the configured forbidden `tenant_code`; a histogram uses only the route template; `POST /payments/{payment_id}` is a critical route.

Expected results: `tenant_code` is classified dynamic and reported as a violation (high risk); `cloud.region` is variable; `http.route` and `status_class` are stable; the histogram is low risk. The sampling recommendation names tail sampling for the payment route and notes that it requires a Collector-side processor. Conclusions are labeled heuristic without an AST parser.

Non-goal: do not expose values, and do not recommend a strategy without naming its prerequisite infrastructure.
