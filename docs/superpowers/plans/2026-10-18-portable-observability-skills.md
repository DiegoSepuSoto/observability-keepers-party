# Portable Observability Skills Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver five independent, portable OpenTelemetry skills for OpenCode, Claude Code, and Codex, with English installation documentation and automated package validation.

**Architecture:** Keep canonical skill packages under `skills/`, with one standard `SKILL.md` per capability and the onboarding YAML template bundled inside `obs-init`. Skills share guardrails by repeating their concise requirements and use only host-neutral repository inspection and editing capabilities. A Python/pytest validation suite checks metadata, templates, and required instruction contracts; it is a development tool, not a product CLI.

**Tech Stack:** Markdown, YAML, Python 3.10+, pytest, PyYAML.

**Spec:** `docs/superpowers/specs/2026-10-18-portable-observability-skills-design.md`

## Global Constraints

- All repository documentation, skill instructions, examples, and generated user-facing text must be in English.
- The audited repository owns its state in `.observability/config.yaml`.
- Generate maturity `baseline`, telemetry standard `opentelemetry`, and the exact contract values in the spec.
- Never use `user_id`, `email`, `account_id`, `order_id`, or `transaction_id` as metric labels.
- Require asynchronous, non-blocking telemetry export and fail-silent behavior; prefer `BatchSpanProcessor` for traces.
- Require W3C `traceparent` propagation in Kafka, RabbitMQ, SQS, and other asynchronous message headers.
- Verify source implementation with AST or targeted regex/search evidence; YAML alone is not proof.
- Limit each skill run to one or two prioritized actions.
- Do not fabricate SLO, MTTD, MTTR, affected-user, or coverage figures when evidence is missing.
- Do not add a CLI, OpenCode command wrappers, telemetry runtime, or automatic application-source edits.
- Do not create commits as part of implementation unless Diego requests them.

## Review Focus

- Existing `.observability/config.yaml` or an unrecognized stack must not cause `obs-init` to overwrite data or guess; cover with `test_obs_init_preserves_existing_contract` and `test_obs_init_treats_unknown_stack_as_unknown`.
- YAML may claim instrumentation that is absent from source; cover with `test_obs_audit_requires_source_evidence`.
- Dynamic identifiers may leak into metric labels, especially in metric-builder calls; cover with `test_skills_forbid_dynamic_metric_labels`.
- Queue instrumentation may omit context propagation or block business paths; cover with `test_obs_audit_checks_async_guardrails`.
- Missing SLOs or critical routes make numeric impact/coverage unknowable; cover with `test_obs_impact_reports_unknown_without_inputs` and `test_obs_score_reports_unknown_without_routes`.

---

### Task 1: Onboarding Skill and Contract Template

**Files:**
- Create: `.gitignore`
- Create: `requirements-dev.txt`
- Create: `tests/test_skill_contracts.py`
- Create: `skills/obs-init/SKILL.md`
- Create: `skills/obs-init/references/observability-config.yaml`

**Interfaces:**
- Produces the canonical YAML template used by `obs-init` and validated by later tasks.
- `tests/test_skill_contracts.py` exposes `read_skill(name: str) -> str` and `read_frontmatter(name: str) -> dict[str, object]` for all subsequent tests.

- [ ] **Step 1: Declare the test dependencies**

Add `pytest` and `PyYAML` to `requirements-dev.txt`; keep production/runtime dependencies empty. Ignore `.venv/`, `__pycache__/`, and `.pytest_cache/` in `.gitignore` so local test runs do not dirty the repository.

- [ ] **Step 2: Write failing onboarding contract tests**

Add tests named `test_obs_init_metadata_is_portable`, `test_baseline_config_matches_requested_schema`, `test_obs_init_preserves_existing_contract`, and `test_obs_init_treats_unknown_stack_as_unknown`. The contract test must parse the template with `yaml.safe_load` and assert every key and value from the spec, including all forbidden labels and all three pillar sections. The instruction tests must assert explicit non-overwrite and uncertainty behavior in the skill text.

- [ ] **Step 3: Run the focused tests and confirm they fail because the onboarding package is absent**

Run: `python -m pytest tests/test_skill_contracts.py -k 'obs_init or baseline_config' -q`

Expected: FAIL because `obs-init` and its YAML template do not exist yet.

- [ ] **Step 4: Implement the onboarding package**

Create the portable `name`/`description` frontmatter and instructions to inspect `package.json`, `go.mod`, `requirements.txt`, and equivalent manifests; infer the service name only from reliable evidence; create `.observability/config.yaml` from the bundled template; preserve an existing config; and print one concise English status line. Add the exact baseline YAML from the spec at `skills/obs-init/references/observability-config.yaml`.

- [ ] **Step 5: Run the focused tests and confirm they pass**

Run: `python -m pytest tests/test_skill_contracts.py -k 'obs_init or baseline_config' -q`

Expected: PASS for all selected onboarding and schema tests.

### Task 2: SDD Instrumentation Guide Skill

**Files:**
- Modify: `tests/test_skill_contracts.py`
- Create: `skills/obs-guide/SKILL.md`

**Interfaces:**
- Consumes the canonical contract at `.observability/config.yaml` and a user-specified SDD feature file.
- Produces focused guidance and boilerplate in the response; it does not edit application source files.

- [ ] **Step 1: Write failing guide contract tests**

Add `test_obs_guide_limits_scope_and_priorities` and `test_obs_guide_applies_cardinality_and_sanitization_rules`. Assert the skill requires reading the feature and config, limits recommendations to one or two actions, keeps boilerplate scoped to the target function, and prohibits dynamic metric labels and unsanitized sensitive values.

- [ ] **Step 2: Run the guide tests and confirm they fail because the skill is absent**

Run: `python -m pytest tests/test_skill_contracts.py -k obs_guide -q`

Expected: FAIL because `skills/obs-guide/SKILL.md` does not exist.

- [ ] **Step 3: Implement `skills/obs-guide/SKILL.md`**

Give it portable frontmatter and a short workflow: require the active feature path and contract, identify the target code path from the spec, provide only relevant spans/counters/histograms, keep dynamic identifiers out of metric labels, use safe span/log attributes, and return at most two priority actions in English. If inputs are missing, report the one prerequisite.

- [ ] **Step 4: Run the guide tests and confirm they pass**

Run: `python -m pytest tests/test_skill_contracts.py -k obs_guide -q`

Expected: PASS for both guide contract tests.

### Task 3: Static Audit and SDD Task Skill

**Files:**
- Modify: `tests/test_skill_contracts.py`
- Create: `skills/obs-audit/SKILL.md`

**Interfaces:**
- Consumes local source, `.observability/config.yaml`, and existing `.sdd/observability/` tasks.
- Produces a compact report and at most two prioritized Markdown tasks under `.sdd/observability/`.

- [ ] **Step 1: Write failing audit contract tests**

Add `test_obs_audit_requires_source_evidence`, `test_obs_audit_marks_regex_as_heuristic`, `test_obs_audit_checks_async_guardrails`, and `test_obs_audit_caps_sdd_tasks`. Assert YAML is not accepted as proof, AST evidence is distinguished from regex/search heuristics, metric-label/export/queue-propagation checks are explicit, and generated tasks contain evidence, required change, and acceptance criteria.

- [ ] **Step 2: Run the audit tests and confirm they fail because the skill is absent**

Run: `python -m pytest tests/test_skill_contracts.py -k obs_audit -q`

Expected: FAIL because `skills/obs-audit/SKILL.md` does not exist.

- [ ] **Step 3: Implement `skills/obs-audit/SKILL.md`**

Define source-first inspection: use an available language-aware AST parser when practical, otherwise targeted regex/search and label conclusions heuristic. Check dynamic metric labels, asynchronous fail-silent export, `BatchSpanProcessor`, and W3C `traceparent` headers for Kafka/RabbitMQ/SQS. Never claim runtime coverage from static checks. Create unique sequential `sdd-XXX-<feature>.md` tasks, avoid duplicates, and emit no more than two actions.

- [ ] **Step 4: Run the audit tests and confirm they pass**

Run: `python -m pytest tests/test_skill_contracts.py -k obs_audit -q`

Expected: PASS for all audit contract tests.

### Task 4: Business Impact Skill

**Files:**
- Modify: `tests/test_skill_contracts.py`
- Create: `skills/obs-impact/SKILL.md`

**Interfaces:**
- Consumes configured SLO/SLI values, audit evidence, and critical-path coverage when present.
- Produces an English executive summary of three to five lines.

- [ ] **Step 1: Write failing impact contract tests**

Add `test_obs_impact_summary_length_and_business_language` and `test_obs_impact_reports_unknown_without_inputs`. Assert three-to-five-line output, customer-visible framing for availability/latency/errors, and explicit unavailability rather than fabricated MTTD, MTTR, affected-user, or SLO values when evidence is missing.

- [ ] **Step 2: Run the impact tests and confirm they fail because the skill is absent**

Run: `python -m pytest tests/test_skill_contracts.py -k obs_impact -q`

Expected: FAIL because `skills/obs-impact/SKILL.md` does not exist.

- [ ] **Step 3: Implement `skills/obs-impact/SKILL.md`**

Instruct the agent to translate verified telemetry into three-to-five lines, tie HTTP 5xx and p95 latency to customer experience and configured SLOs, and estimate MTTD/MTTR or affected users only when inputs support the calculation. Otherwise say the estimate is unavailable.

- [ ] **Step 4: Run the impact tests and confirm they pass**

Run: `python -m pytest tests/test_skill_contracts.py -k obs_impact -q`

Expected: PASS for both impact contract tests.

### Task 5: Three-Pillar Maturity Score Skill

**Files:**
- Modify: `tests/test_skill_contracts.py`
- Create: `skills/obs-score/SKILL.md`

**Interfaces:**
- Consumes the config and static evidence from detected critical routes.
- Produces a compact ASCII/tree scorecard for logs, metrics, and traces.

- [ ] **Step 1: Write failing score contract tests**

Add `test_obs_score_uses_per_pillar_route_evidence` and `test_obs_score_reports_unknown_without_routes`. Assert the skill uses detected critical routes as a denominator, reports per-pillar percentages only when that denominator exists, and distinguishes static evidence from runtime coverage.

- [ ] **Step 2: Run the score tests and confirm they fail because the skill is absent**

Run: `python -m pytest tests/test_skill_contracts.py -k obs_score -q`

Expected: FAIL because `skills/obs-score/SKILL.md` does not exist.

- [ ] **Step 3: Implement `skills/obs-score/SKILL.md`**

Count a route as statically covered by traces only with source evidence of a server span; by metrics only with a relevant counter or histogram; and by logs only with a structured log carrying trace context. Use all detected critical routes as each pillar's denominator, report `unknown` when none can be established, and never imply runtime coverage.

- [ ] **Step 4: Run the score tests and confirm they pass**

Run: `python -m pytest tests/test_skill_contracts.py -k obs_score -q`

Expected: PASS for both score contract tests.

### Task 6: Cross-Platform Installation and Repository Documentation

**Files:**
- Create: `README.md`
- Create: `CONTRIBUTING.md`
- Create: `docs/installation.md`
- Modify: `tests/test_skill_contracts.py`

**Interfaces:**
- Documents canonical skill packages under `skills/` and installation into OpenCode, Claude Code, and Codex native discovery paths.
- Does not add platform-specific command wrappers or claim a universal invocation command.

- [ ] **Step 1: Write failing documentation contract tests**

Add `test_installation_documents_all_native_skill_paths` and `test_documentation_does_not_promise_universal_invocation`. Assert documentation covers `.opencode/skills/`, `.claude/skills/`, and `.agents/skills/`, explains copy/link installation, and describes invoking by skill name using each host's conventions.

- [ ] **Step 2: Run the documentation tests and confirm they fail because the docs are absent**

Run: `python -m pytest tests/test_skill_contracts.py -k 'installation or invocation' -q`

Expected: FAIL because the installation guide and root documentation do not exist.

- [ ] **Step 3: Write the English documentation**

Describe the five skills and their outputs in `README.md`; give exact per-host discovery paths and installation steps in `docs/installation.md`; describe test setup and contribution expectations in `CONTRIBUTING.md`. Explain that the skills have common content but host-specific activation syntax, and that no license is included until the repository owner selects one.

- [ ] **Step 4: Run the documentation tests and confirm they pass**

Run: `python -m pytest tests/test_skill_contracts.py -k 'installation or invocation' -q`

Expected: PASS for the documentation contract tests.

### Task 7: Full Package Validation

**Files:**
- Modify: `tests/test_skill_contracts.py`
- Modify: all five skill packages as needed to satisfy validation

- [ ] **Step 1: Add suite-wide metadata and guardrail tests**

Add `test_all_skills_have_matching_portable_frontmatter` and `test_skills_forbid_dynamic_metric_labels`. Check all five directory names against their `name` frontmatter, require non-empty descriptions, and verify each instrumentation-related skill includes cardinality, async/fail-silent export, event propagation, source-evidence, and drip-feeding constraints.

- [ ] **Step 2: Run the complete suite and inspect failures**

Run: `python -m pytest -q`

Expected: Any failures identify missing prompt or documentation requirements; no application code is involved.

- [ ] **Step 3: Make the smallest documentation or skill-text corrections**

Update only the affected package or docs. Preserve host neutrality and keep each skill self-contained.

- [ ] **Step 4: Run the full suite and confirm it passes**

Run: `python -m pytest -q`

Expected: PASS for all package, YAML, skill, and installation documentation checks.

## Execution Notes

- Install test dependencies in a virtual environment with `python3 -m venv .venv` followed by `.venv/bin/python -m pip install -r requirements-dev.txt`.
- The test suite validates static package contracts; it does not execute an LLM or prove runtime OpenTelemetry coverage.
- No commits are included in the task steps. The user has already committed the approved design and did not request phase commits.

## Plan Self-Review

- **Spec coverage:** All five skills, the exact baseline contract, guardrails, SDD tasks, platform portability, English-only content, installation docs, repository docs, and automated validation map to tasks above.
- **Step scan:** Each task starts with a failing test, implements one bounded package or document, and runs a focused passing check.
- **Interface consistency:** All skills read the audited repository config; only `obs-init` creates it. The audit's SDD output path and score denominator match the spec.
- **Review focus:** Existing config/unknown stack, YAML-only assertions, dynamic labels, async queue boundaries, and missing business inputs each have named tests.
- **Proportion:** The plan records file boundaries, acceptance tests, and prompt contracts without specifying implementation bodies that the skill descriptions already determine.
