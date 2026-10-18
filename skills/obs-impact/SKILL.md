---
name: obs-impact
description: Translate verified observability coverage and configured SLOs/SLIs into a concise customer-impact summary for product stakeholders.
---

# Explain Observability Impact

Read `.observability/config.yaml`, relevant audit evidence, and verified coverage for the critical path. SLO/SLI fields are optional and user-maintained; the baseline template does not invent targets. Use only facts supported by these inputs and keep the summary in English.

## Executive summary

Return **three to five lines**. Connect telemetry to customer experience: explain what HTTP 5xx errors mean for the affected action, what p95 latency means for perceived responsiveness, and how the configured SLO/SLI target is being met or missed when evidence exists. Include no more than one or two prioritized actions.

Before stating a percentage of users impacted, require evidence for both distinct affected users (or a clearly defined affected-user cohort) and a matching user-population denominator over the same observation window. Request counts do not establish distinct users; retries and unequal user activity can distort them. If only request traffic exists, report request impact and mark user impact unavailable. Estimate MTTD or MTTR only when incident, alert, and recovery records support the calculation. Static code coverage alone does not establish detection or recovery time.

If the config, SLO/SLI target, traffic data, or incident evidence is missing, state that the corresponding estimate is **unavailable**. Do not invent targets, error rates, latency values, MTTD, MTTR, or affected-user percentages. If `.observability/config.yaml` itself is missing, report `obs-init` as the single prerequisite.

Keep the language direct and business-focused. Do not list raw telemetry fields or produce a technical backlog.

## Telemetry guardrails

- Never use `user_id`, `email`, `account_id`, `order_id`, or `transaction_id` as metric labels. Keep dynamic identifiers out of metric dimensions; include them in spans or logs only when necessary and sanitized.
- Never collect or seed secrets, credentials, raw request bodies, or unnecessary personal data.
- Telemetry export must be asynchronous and non-blocking with fail-silent behavior; use `BatchSpanProcessor` for traces.
- For Kafka, RabbitMQ, SQS, and other asynchronous boundaries, require W3C trace context propagation through message headers using `traceparent`.
- Treat coverage as verified only when supported by source evidence. Use AST evidence when available; label regex/search evidence as heuristic. YAML alone is not proof, and static evidence is not runtime coverage.
- Keep any recommendations to one or two priority actions.
