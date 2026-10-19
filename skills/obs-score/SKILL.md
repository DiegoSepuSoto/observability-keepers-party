---
name: obs-score
description: Produce a compact, source-evidence scorecard for trace, metric, and log coverage across critical routes in a repository.
---

# Score Observability Coverage

Read `.observability/config.yaml` and inspect source code for critical customer-facing routes or equivalent request handlers. Use only repository evidence, keep the report in English, and limit findings to one or two priority actions.

## Output style

Use the enterprise style by default: concise, direct, technical, and free of fantasy metaphors. Use the Adventuring Party style only when the request invoking this skill contains the exact phrase `fantasy naming`. Keep all responses in English. In that style, add at most one brief character-framed sentence or label; preserve technical facts, evidence limits, privacy rules, and this skill's output constraints exactly. Fantasy language may frame a fact but must never obscure or replace it. Do not change commands, error codes, file paths, filenames, OpenTelemetry attributes, or measured values.

When the Adventuring Party style is active, speak as the **Cartographer**: a careful scout who maps verified route evidence. The scorecard shows the party's readiness; keep every numerator, denominator, percentage, and unknown value explicit.

## Static evidence

- Use an available language-aware AST parser when practical. Otherwise use targeted regex/search and label the result heuristic, with file and line references.
- A YAML declaration is not proof that the corresponding instrumentation exists in source.
- This is a static scorecard, not a runtime coverage measurement. Never claim runtime coverage.
- Count metric coverage only when dimensions are stable and low-cardinality; identifiers such as `user_id`, `email`, `account_id`, `order_id`, or `transaction_id` are not valid metric dimensions. Keep dynamic identifiers out of the scorecard.
- Never expose secrets, credentials, raw request bodies, or unnecessary personal data in the scorecard.

## Coverage calculation

Use the same set of detected critical routes as the denominator for each pillar. Count a route as statically covered only when source evidence supports the relevant requirement:

- **Traces:** the route creates or enters a server span through an OpenTelemetry wrapper.
- **Metrics:** the route records an applicable counter or histogram using stable, low-cardinality dimensions such as route template, method, or status class.
- **Logs:** the route emits a structured log with trace context, including a trace ID.

For each pillar, report `covered routes / detected critical routes` and calculate the percentage from those counts. If no critical routes can be established, report `unknown` for all percentages and state that no critical routes were detected. Do not invent a denominator. Mark regex-based route or instrumentation detection as heuristic.

## Output

Use a compact ASCII tree, for example:

```text
Observability score — static source evidence
├─ Traces: 2/3 routes — 67%
├─ Metrics: 1/3 routes — 33%
└─ Logs: 3/3 routes — 100%
```

Show the configured maturity level only as declared in the config; do not infer or upgrade it from this score. Add at most two concise actions, ordered by customer impact. If `.observability/config.yaml` is missing, report `obs-init` as the single prerequisite and stop.
