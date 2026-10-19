---
name: obs-init
description: Initialize an OpenTelemetry observability contract from project manifests, stopping when service selection is ambiguous.
---

# Initialize the Observability Contract

Run this skill from the root of the repository being onboarded. Keep the work local to that repository and return one concise status line in English.

## Procedure

1. Check whether `.observability/config.yaml` already exists. If it does, **do not overwrite** or merge it. Report that the contract already exists and stop.
2. Inspect relevant project manifests without dumping their full contents. Check `package.json`, `go.mod`, `requirements.txt`, `pyproject.toml`, `Cargo.toml`, and equivalent manifests. Include service manifests referenced by workspace configuration; ignore generated or vendored dependencies.
3. Identify the likely stack only from manifest evidence. For example, `package.json` indicates a Node.js project, `go.mod` indicates Go, and `requirements.txt` or Python project metadata indicates Python. If the evidence is incomplete or contradictory, record the stack as unknown; **do not guess**.
4. Check whether the relevant manifests identify one service or multiple independent services. If they identify multiple candidates, or conflicting names make the target unclear, **stop before creating `.observability/config.yaml`**. Report the candidate service names and their manifest paths in one concise English line, then ask which service to initialize or ask the user to run the skill from the selected service root. Manifests that agree on one service identity are not ambiguous.
5. For one unambiguous service, derive `service` from a reliable declared project name when available: `package.json`'s `name`, Python project metadata, or the final module path component in `go.mod`. Use `unnamed-service` when the service is clear but no reliable name is declared.
6. Read the authoritative bundled defaults from `references/observability-config.yaml` relative to this skill. Create `.observability/` if needed and write the template to `.observability/config.yaml`, changing only `service` when reliable evidence provides a name. Keep `maturity_level` at `baseline`.
7. Print one concise English line confirming creation and naming the detected stack or `unknown`. Keep the ambiguity response to one concise English line as well.

The bundled template is the source of observability defaults. Onboarding initializes the contract; it does not audit source instrumentation.

Do not modify application source code as part of onboarding.
