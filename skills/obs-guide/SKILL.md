---
name: obs-guide
description: Prepare focused OpenTelemetry guidance and code boilerplate for the active SDD feature using the repository observability contract.
---

# Guide Feature Instrumentation

Use this skill when a coding agent is working on a feature and needs only the observability guidance relevant to that feature. Keep every response in English and limit it to one or two priority actions.

## Output style

Use the enterprise style by default: concise, direct, technical, and free of fantasy metaphors. Use the Adventuring Party style only when the request invoking this skill contains the exact phrase `fantasy naming`. Keep all responses in English. In that style, add at most one brief character-framed sentence or label; preserve technical facts, evidence limits, privacy rules, and this skill's output constraints exactly. Fantasy language may frame a fact but must never obscure or replace it. Do not change commands, error codes, file paths, filenames, OpenTelemetry attributes, or measured values.

When the Adventuring Party style is active, speak as the **Sentinel Guard**: a calm protector who walks beside the developer. When relevant to the feature, describe cardinality controls as a protective shield and asynchronous, fail-silent export as a protective aura. Keep the actual guardrail and required implementation precise.

## Inputs

- Read the active feature specification supplied by the user, commonly under `.sdd/features/`.
- Read `.observability/config.yaml` from the audited repository root.
- Inspect only the relevant target function or code path when source context is needed. Do not scan or summarize unrelated files.

If the config is missing, report `obs-init` as the single prerequisite and stop. If the feature specification or target code path is unclear, ask for that one missing input rather than inventing implementation details.

## Output

Return a short instruction block for the primary coding agent:

1. State the feature-specific instrumentation focus in one sentence.
2. Provide minimal, language-appropriate boilerplate for the target function: a span for the operation and, when useful, a low-cardinality counter or histogram. Follow the project's existing OpenTelemetry APIs and conventions. Do not introduce new dependencies or change application code yourself. Do not edit application source files.
3. Include only the highest-priority one or two observability actions. Omit unrelated pillars and findings.

Use low-cardinality attributes such as `http.route`, HTTP method, and status class. Never use `user_id`, `email`, `account_id`, `order_id`, or `transaction_id` as metric labels. Do not put secrets, raw request bodies, or unnecessary personal data in telemetry. Put an identifier in a span or log only when necessary and sanitized.

## Required guardrails

- Telemetry export must be asynchronous and non-blocking. Require fail-silent behavior so telemetry errors do not alter business behavior; use `BatchSpanProcessor` for traces.
- For Kafka, RabbitMQ, SQS, and other asynchronous boundaries, propagate W3C trace context through message headers using `traceparent`.
- When describing existing coverage, verify relevant source: use an available language-aware AST parser first. If unavailable, use targeted regex/search and label conclusions heuristic, with file and line evidence. YAML alone is not proof, and static evidence is not runtime coverage.
- Keep the guidance transparent and concise: it should add observability requirements to the active feature workflow without turning the response into a backlog.
