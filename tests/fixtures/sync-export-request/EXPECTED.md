# Expected behavior: sync-export-request

Applies to `obs-audit` and `obs-guide`.

Inputs: a request handler uses `SimpleSpanProcessor`, which may synchronously export spans on the request path.

Expected results: the finding cites the processor setup and request path, explains the potential blocking and business-impact risk, and labels regex-only evidence heuristic. It does not claim a measured latency impact.

Non-goal: do not change application code or infer exporter runtime behavior.
