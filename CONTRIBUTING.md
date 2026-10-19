# Contributing

## Language and scope

Keep skill instructions, documentation, examples, and generated user-facing text in English. Keep each capability independent under `skills/<name>/`; do not add a custom CLI, host-specific command wrapper, or shared runtime dependency.

## Skill changes

- Keep the standard `name` and `description` YAML frontmatter valid.
- Make the skill usable on OpenCode, Claude Code, and Codex without relying on a platform-only API.
- Preserve each skill's output limit and keep telemetry guardrails specific to its responsibility. `obs-guide` and `obs-audit` carry full instrumentation guardrails; `obs-score` checks route evidence, metric cardinality, and privacy; `obs-impact` protects evidence integrity and privacy; `obs-init` follows the bundled contract template and handles service ambiguity safely.
- Keep `obs-init`'s template inside its skill directory at `references/observability-config.yaml`.
- Do not state that YAML proves source instrumentation or that static inspection proves runtime coverage.
- Keep generated audit work in the audited repository's `.sdd/observability/` directory.

## Validation

Set up the development environment and run the full package checks:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m pytest -q
```

The tests check package and documentation contracts. They do not execute an AI agent, so review changes to skill instructions against the approved design and exercise them in each host when practical.

## Licensing

No license has been selected for this repository. Confirm the repository owner's choice before adding a license file or publishing a public distribution.
