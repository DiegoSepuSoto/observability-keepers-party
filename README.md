# Observability Skills for AI Agents

Five independent, portable skills that bring OpenTelemetry guidance into spec-driven development. Install the skill folders into the native discovery directory for OpenCode, Claude Code, or Codex; no custom CLI or build step is required.

## Skills

| Skill | Purpose |
| --- | --- |
| `obs-init` | Detect the repository stack and create `.observability/config.yaml` from the bundled baseline template. |
| `obs-guide` | Prepare focused observability guidance and boilerplate for an active SDD feature. |
| `obs-audit` | Check source evidence against the observability contract and create up to two prioritized SDD tasks. |
| `obs-impact` | Explain verified telemetry and SLO/SLI evidence in a three-to-five-line customer-impact summary. |
| `obs-score` | Show static logs, metrics, and traces coverage for detected critical routes. |

Each skill keeps instructions specific to its task. `obs-guide` and `obs-audit` carry the full instrumentation guardrails; `obs-score` focuses on route evidence, metric cardinality, and privacy; `obs-impact` focuses on verified business claims and privacy; and `obs-init` uses its bundled template and stops when service selection is ambiguous. Static checks are not represented as runtime coverage.

## Response style

All skill responses remain in English. Enterprise style is the default. Include `fantasy naming` or `fantasy-naming` in a skill request, in any letter case, to opt into the Adventuring Party voice; paraphrases do not activate it. The selected skill adds at most one brief character-framed sentence while preserving technical facts and its existing output limits. The roles are Cartographer (`obs-init`, `obs-score`), Sentinel Guard (`obs-guide`), Spectral Inquisitor (`obs-audit`), and Troubadour (`obs-impact`). This is a natural-language convention for portable skills, not a CLI option or shared runtime.

## Installation

Copy or link any complete skill directory under the target tool's native skill path. Keep each folder intact so `obs-init` can read its bundled template. See [the installation guide](docs/installation.md) for platform-specific paths and activation examples.

The skills support SDD artifacts without requiring a specific SDD framework. See [the SDD conventions](docs/sdd-conventions.md) for the expected feature-spec and audit-task formats.

## Forking and creating your own version

Everyone is free to fork this repository, modify the skills, create an independent version, and publish or redistribute it under the [MIT License](LICENSE). Keep the copyright and permission notice with copies or substantial portions of the software, as the license requires.

## Development

The automated checks validate skill metadata, the baseline YAML contract, required instruction contracts, and installation documentation. They do not run an AI model or prove application runtime coverage.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m pytest -q
```

See [CONTRIBUTING.md](CONTRIBUTING.md) before changing a skill.
