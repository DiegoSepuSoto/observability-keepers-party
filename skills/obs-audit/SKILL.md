---
name: obs-audit
description: Audit a repository's OpenTelemetry implementation against its observability contract and create only the highest-priority executable SDD task(s).
---

# Audit Observability

Run from the root of the repository being audited. Keep the report in English and return no more than one or two prioritized actions. Do not edit application source code.

## Inputs and preflight

- Read `.observability/config.yaml` as the expected contract, not as proof of implementation.
- Inspect source files for critical HTTP routes, RPC handlers, scheduled jobs, and message producers or consumers. Focus on paths that affect customer requests or important asynchronous work.
- Check existing open tasks under `.sdd/observability/` before creating new ones.
- If the contract is missing, report `obs-init` as the single prerequisite and stop. Do not produce speculative findings.

## Source verification

Verify OpenTelemetry wrappers in source code. A YAML declaration alone is never proof that spans, metrics, or structured logs exist.

- Use a language-aware AST parser only when it is already available in the project or environment. Do not install dependencies or modify the audited project to perform an audit.
- If AST inspection is unavailable, use targeted regex or text search around relevant call sites. Label every such conclusion as a **heuristic**, include the file and line evidence, and state that static search may miss indirect wrappers.
- Distinguish verified source evidence, heuristic evidence, missing source evidence, and runtime behavior you cannot establish statically. Never claim runtime coverage from this audit.

## Guardrail checks

1. **Metric cardinality:** Inspect metric construction and label/attribute arguments for dynamic values. Never allow `user_id`, `email`, `account_id`, `order_id`, or `transaction_id` as metric labels. Such values may appear in spans or logs only when necessary and sanitized. Also check that route labels use stable route templates rather than raw paths or identifiers.
2. **Export performance and failure isolation:** Verify trace export uses an asynchronous, non-blocking pattern such as OpenTelemetry `BatchSpanProcessor`; flag synchronous `SimpleSpanProcessor` use on request paths. Check that exporter failures are fail-silent and cannot change business behavior. Report only what source evidence supports.
3. **Event context propagation:** For Kafka, RabbitMQ, SQS, and other asynchronous boundaries, inspect producer and consumer code for W3C context injection and extraction through headers, including `traceparent`. Do not infer propagation from the configured `w3c` value alone.
4. **Pillar coverage:** Compare actual source evidence for spans, counters/histograms, and structured logs with trace, metric, and log requirements in the contract. Do not demand custom metrics when framework defaults satisfy the configured scope.
5. **Data safety:** Flag secrets, credentials, raw request bodies, or unnecessary personal data in telemetry attributes or log fields.

## Output and SDD tasks

Print a compact report that names the audit scope, distinguishes evidence from heuristics, and gives at most two prioritized findings. If no actionable gap is found, say so in one concise sentence.

For each selected finding, create one executable Markdown task under `.sdd/observability/` using the filename pattern `sdd-XXX-<feature>.md`, where `XXX` is the next unused three-digit sequence. Before writing, avoid any duplicate or equivalent open task. Create no more than two tasks in one run; a second task must be independently urgent. Each task must contain:

- A concise title and priority.
- Concrete evidence with source file and line references, marked as heuristic when applicable.
- Why the gap matters to customer reliability or the stated contract.
- The required source change, without implementing it.
- Testable acceptance criteria.

Select findings by customer impact and risk reduction, not by scan order. Do not print a backlog of lower-priority findings. Do not claim a task was written unless the file was actually created.
