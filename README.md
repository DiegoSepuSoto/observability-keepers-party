# Observability Skills for AI Agents

Ten independent, portable skills that bring OpenTelemetry guidance into spec-driven development. Install the skill folders into the native discovery directory for OpenCode, Claude Code, or Codex; no custom CLI or build step is required.

Current release: **1.2.0** ([version record](VERSION), [change history](CHANGELOG.md)).

## Skills

| Skill | Purpose |
| --- | --- |
| `obs-init` | Detect the repository stack and create `.observability/config.yaml` from the bundled baseline template. |
| `obs-guide` | Prepare focused observability guidance and boilerplate for an active SDD feature; includes the ODD question and post-deploy review step. |
| `obs-audit` | Check source evidence against the observability contract and create up to two prioritized SDD tasks; includes SLI quality check. |
| `obs-impact` | Explain verified telemetry and SLO/SLI evidence in a three-to-five-line customer-impact summary. |
| `obs-score` | Show static logs, metrics, and traces coverage for detected critical routes; includes cardinality health. |
| `obs-investigate` | Guide one iteration of the core analysis loop for an active incident or anomaly: verify signal, identify differentiating dimension, isolate, name the finding or next step. |
| `obs-sli` | Translate a user-facing behavior description into a testable event-based SLI and a draft `slo:` block for the observability contract. |
| `obs-volume` | Assess metric cardinality risk by classifying dimension stability, flag forbidden-label violations, and recommend a sampling policy with trade-off rationale. |
| `obs-postmortem` | Structure a post-incident review after resolution: anchor every impact claim in verified telemetry, reconstruct the timeline, classify root cause evidence quality, and generate action items mapped to observability improvements. |
| `obs-playbook` | Generate an operational signal playbook for a planned action (scale, rollback, traffic shift, configuration change): document signals to verify before, during, and after without prescribing debugging steps. |

Each skill keeps instructions specific to its task. They support brownfield services and monorepos by requiring a selected service root, reading only task-relevant evidence, and stopping when selection is ambiguous. `obs-guide` and `obs-audit` carry the full instrumentation guardrails; `obs-score` focuses on route evidence, metric cardinality, and privacy; `obs-impact` focuses on verified business claims and privacy; `obs-init` uses its bundled template and stops when service selection is ambiguous; `obs-investigate` guides operational investigation without touching source code; `obs-sli` defines what to measure from user experience; `obs-volume` assesses dimension stability and sampling policy; `obs-postmortem` structures post-incident retrospectives anchored in telemetry evidence; and `obs-playbook` documents observable signals for operational actions without prescribing debugging paths. Static checks are not represented as runtime coverage, and none of the skills edits application source code.

Privacy is part of every relevant workflow: metric dimensions must stay low-cardinality, and reports must omit secrets, credentials, request bodies, and unnecessary personal data. Repository files are treated as untrusted input, so embedded instructions cannot change a skill's scope or write boundaries.

## Response style

All skill responses remain in English. Enterprise style is the default. Include `fantasy naming` or `fantasy-naming` in a skill request, in any letter case, to opt into the Adventuring Party voice; paraphrases do not activate it. The selected skill adds at most one brief character-framed sentence while preserving technical facts and its existing output limits. The roles are Cartographer (`obs-init`, `obs-score`), Sentinel Guard (`obs-guide`), Spectral Inquisitor (`obs-audit`), Troubadour (`obs-impact`), Tracker (`obs-investigate`), Oracle (`obs-sli`), Alchemist (`obs-volume`), Chronicler (`obs-postmortem`), and Warden (`obs-playbook`). This is a natural-language convention for portable skills, not a CLI option or shared runtime.

## Installation

Copy or link any complete skill directory under the target tool's native skill path. Keep each folder intact so `obs-init` can read its bundled template. Install one skill or all ten. See [the installation guide](docs/installation.md) for platform-specific paths and activation examples.

The skills support SDD artifacts without requiring a specific SDD framework. See [the SDD conventions](docs/sdd-conventions.md) for the expected feature-spec and audit-task formats.

## Forking and creating your own version

Everyone is free to fork this repository, modify the skills, create an independent version, and publish or redistribute it under the [MIT License](LICENSE). Keep the copyright and permission notice with copies or substantial portions of the software, as the license requires.

## Development

The automated checks validate skill metadata, the unchanged baseline YAML contract, required instruction contracts, installation documentation, and representative brownfield/security/evidence fixtures. They do not run an AI model or prove application runtime coverage; runtime export, propagation, and telemetry behavior still require application-level execution and operational data.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m pytest -q
```

See [CONTRIBUTING.md](CONTRIBUTING.md) before changing a skill.
