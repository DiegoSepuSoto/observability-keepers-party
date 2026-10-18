---
name: obs-init
description: Initialize a repository's OpenTelemetry observability contract by identifying its service and technology stack from project manifests.
---

# Initialize the Observability Contract

Run this skill from the root of the repository being onboarded. Keep the work local to that repository and return one concise status line in English.

## Procedure

1. Check whether `.observability/config.yaml` already exists. If it does, **do not overwrite** or merge it. Report that the contract already exists and stop.
2. Inspect relevant project manifests without dumping their full contents. Check `package.json`, `go.mod`, `requirements.txt`, `pyproject.toml`, `Cargo.toml`, and equivalent manifests when present.
3. Identify the likely stack only from manifest evidence. For example, `package.json` indicates a Node.js project, `go.mod` indicates Go, and `requirements.txt` or Python project metadata indicates Python. If the evidence is incomplete or contradictory, record the stack as unknown in your response; **do not guess**.
4. Derive `service` from a reliable declared project name when available: `package.json`'s `name`, Python project metadata, or the final module path component in `go.mod`. Use `unnamed-service` when no reliable name is declared.
5. Read the bundled template at `references/observability-config.yaml` relative to this skill. Create `.observability/` if needed and write the template to `.observability/config.yaml`, changing only `service` when reliable evidence provides a name. Keep `maturity_level` at `baseline`.
6. Print one concise English line confirming the contract was created and naming the detected stack or `unknown`.

## Observability guardrails

- Never define `user_id`, `email`, `account_id`, `order_id`, or `transaction_id` as metric labels. Keep such values out of metric dimensions; use spans or logs only when appropriate and sanitized.
- Telemetry export must be asynchronous and non-blocking, with fail-silent behavior so exporter failure cannot change business behavior. Use `BatchSpanProcessor` for trace export.
- Preserve W3C trace context by propagating `traceparent` through asynchronous message headers, including Kafka, RabbitMQ, and SQS.
- A declaration in `.observability/config.yaml` is a contract, not evidence that source instrumentation exists. Verify implementation in source with AST inspection or targeted regex/search when auditing.
- Do not collect secrets, credentials, raw request bodies, or unnecessary personal data.

Do not modify application source code as part of onboarding.
