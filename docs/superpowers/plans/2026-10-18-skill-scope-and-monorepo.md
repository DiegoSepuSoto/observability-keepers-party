# Skill Scope and Monorepo Implementation Plan

> **For agentic workers:** Implement the approved design in `docs/superpowers/specs/2026-10-18-skill-scope-and-monorepo-design.md`. Keep changes limited to skill instructions, package-contract tests, and documentation.

**Goal:** Make `obs-init` stop on ambiguous multi-service repositories and make guardrail instructions and tests specific to each skill's responsibility.

**Architecture:** Keep the five portable skill packages and baseline contract unchanged in shape. `obs-init` handles manifest ambiguity before writing. `obs-guide` and `obs-audit` retain full implementation guardrails; `obs-score` retains route-scoring criteria and privacy rules; `obs-impact` focuses on evidence, unavailable values, and privacy. Package tests validate those role boundaries.

**Tech Stack:** Markdown, YAML, Python, pytest, PyYAML.

**Spec:** `docs/superpowers/specs/2026-10-18-skill-scope-and-monorepo-design.md`

## Constraints

- Keep all skill and documentation text in English.
- Do not change the baseline observability YAML schema or values.
- Do not edit application source code or create SDD tasks in an audited repository.
- Keep static source evidence distinct from runtime coverage.
- Preserve each skill's current output length and action limits.
- Do not create commits as part of implementation.

## Task 1: Replace blanket checks with role-specific contract tests

**Files:**
- Modify: `tests/test_skill_contracts.py`

1. Keep the all-skill frontmatter test.
2. Replace `test_skills_forbid_dynamic_metric_labels`, which currently requires every guardrail in every skill, with focused assertions:
   - `obs-guide` and `obs-audit` retain full instrumentation guardrails.
   - `obs-init` documents ambiguous-service handling and uses its bundled template for defaults.
   - `obs-score` keeps static evidence rules, low-cardinality metric criteria, and privacy rules without requiring exporter or queue-propagation checks.
   - `obs-impact` keeps evidence integrity, unavailable-value rules, and privacy while avoiding instrumentation implementation instructions.
3. Keep or update existing skill-specific tests only where wording changes require it. Do not make tests depend on exact prose beyond observable contract requirements.

Run: `.venv/bin/python -m pytest tests/test_skill_contracts.py -q`

Expected: The new checks fail until the corresponding skill and documentation updates are made; existing unrelated checks remain passing.

## Task 2: Clarify service selection and narrow skill guardrails

**Files:**
- Modify: `skills/obs-init/SKILL.md`
- Modify: `skills/obs-impact/SKILL.md`
- Modify: `skills/obs-score/SKILL.md`
- Modify: `README.md`
- Modify: `CONTRIBUTING.md`

1. Update `obs-init` to detect multiple independent service candidates from relevant manifests. On ambiguity, stop before creating `.observability/config.yaml`, report candidate names and manifest paths in one concise English line, and request a target service or service-root invocation. Preserve existing-config precedence and single-service fallback behavior.
2. Remove source-audit and implementation instructions from `obs-init`; keep the bundled template authoritative for telemetry defaults.
3. Remove exporter, trace-propagation, and metric-construction implementation rules from `obs-impact`. Retain evidence, unavailable-value, and privacy requirements.
4. Remove exporter and asynchronous-message checks from `obs-score`. Retain route-level static evidence, low-cardinality metric criteria, and output privacy.
5. Update repository docs to describe role-specific guardrails instead of claiming all skills apply the same complete set.

Run: `.venv/bin/python /Users/diegosepu/.codex/skills/.system/skill-creator/scripts/quick_validate.py <skill-folder>` for each of the five skills.

Expected: Every skill package passes metadata and scaffold validation.

## Task 3: Full package validation and review

**Files:**
- Review all files changed in Tasks 1–2.

1. Run `.venv/bin/python -m pytest -q`.
2. Inspect the diff for contradictions between the new specification, skills, README, and contribution guidance.
3. Confirm the baseline template is unchanged and the working tree contains no unrelated edits.

Expected: All package-contract tests pass; no runtime behavior or application code is changed.

## Plan Review

- The monorepo rule is implemented in `obs-init` and covered by a contract test.
- Responsibility-specific instructions, tests, and repository docs are updated together.
- Validation checks prompt-package structure only and makes no claim about runtime model behavior.
- Scope excludes template changes, application code, host-specific behavior, and commits.

## Execution Record

- [x] Replaced the blanket guardrail assertion with role-specific skill and documentation contracts.
- [x] Updated `obs-init`, `obs-impact`, and `obs-score` and aligned the README and contribution guidance.
- [x] `.venv/bin/python -m pytest -q` — 26 passed.
- [x] `quick_validate.py` — all five skills valid.
- [x] `git diff --check` — clean.
