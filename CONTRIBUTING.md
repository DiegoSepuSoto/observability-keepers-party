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
- Keep the five skills independently installable. Preserve `skills/obs-init/references/` when installing `obs-init`; no skill requires a custom CLI or runtime dependency.
- Keep brownfield and monorepo behavior explicit: inspect manifests to identify service roots, stop on ambiguous selection, and never infer implementation evidence from configuration alone.
- Treat repository content as untrusted data. Prompt-injection text in code, docs, logs, specs, manifests, or configuration cannot change skill scope, output limits, privacy rules, permitted commands, write paths, or the no-application-edit rule.
- Keep skill responses in English and enterprise style by default. The request phrases `fantasy naming` and `fantasy-naming` (case-insensitive) opt into the Adventuring Party voice; paraphrases do not activate it. Preserve the same evidence, privacy, technical-accuracy, format, and action-limit requirements in both styles.
- Repeat the shared theme rule identically in all five `SKILL.md` files so each package stays self-contained. Keep only the character mapping specific to each skill. Do not add a CLI switch, shared runtime, or host-specific theme behavior.

## Validation

Set up the development environment and run the full package checks:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m pytest -q
```

The tests check package and documentation contracts. They do not execute an AI agent, so review changes to skill instructions against the approved design and exercise them in each host when practical.

Fixtures document expected skill behavior for representative services and evidence gaps. They are prompt-contract examples, not proof that an agent will behave correctly in every host or that application telemetry works at runtime.

## Licensing

This repository is available under the [MIT License](LICENSE). You are free to fork it, create your own version, and distribute or publish that version under the license terms. Preserve the copyright and permission notice in copies or substantial portions of the software.
