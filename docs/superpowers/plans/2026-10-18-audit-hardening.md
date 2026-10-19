# Audit Hardening Implementation Plan

> **For agentic workers:** Implement the approved design in `docs/superpowers/specs/2026-10-18-audit-hardening-design.md`. Keep changes limited to skill instructions, the baseline template, package tests and fixtures, CI, and documentation.

**Goal:** Make the package contract tests meaningful, make `.observability/config.yaml` the real source of guardrails, give `obs-audit` auditable task state, make `obs-score` reproducible, unify service-root scope, document SDD conventions, harden against untrusted repository content, and add basic repository hygiene.

**Architecture:** Five portable skills stay self-contained; shared rules (theme paragraph, untrusted-content rule) are copied identically and enforced by tests. Fixtures under `tests/fixtures/` describe expected observable behavior and are validated structurally only.

**Tech Stack:** Markdown, YAML, Python, pytest, PyYAML, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-10-18-audit-hardening-design.md`

## Constraints

- Keep all skill and documentation text in English.
- Do not change baseline template parsed values except extending `forbidden_metric_labels` (R-2). Do not change `sampling_ratio` or `mandatory_attributes` (owner decision, R-7).
- Preserve each skill's output length and action limits.
- Do not add a CLI, runtime, or new Python dependency. The owner later selected MIT; add its license file and document reuse terms.
- Do not create commits as part of implementation unless asked.
- Run `.venv/bin/python -m pytest -q` after every task; the suite must stay green at the end of each task.

## Task 1: Test helpers and word-boundary assertions (R-1)

**Files:** Modify `tests/test_skill_contracts.py`

1. Add helpers: `has_word(content, word)` using `re.search(rf"\b{re.escape(word)}\b", ...)`, and `section(content, heading)` returning the text under a `## heading` up to the next `## `.
2. Replace every `"ast" in content`, `"ast" not in content`, `"regex" in/not in content` with `has_word` (acronym `AST` matched case-sensitively on the original text).
3. Add `test_shared_output_style_paragraph_is_identical` (first paragraph of `## Output style` equal across all five skills).
4. Add `test_each_skill_has_its_character_and_opt_in_phrase` for `Cartographer` (`obs-init`, `obs-score`), `Sentinel Guard` (`obs-guide`), `Spectral Inquisitor` (`obs-audit`), `Troubadour` (`obs-impact`), plus the phrase `fantasy naming`.

Run: `.venv/bin/python -m pytest -q`
Expected: pass. Sanity check by temporarily editing one skill's shared paragraph and confirming the new test fails, then revert.

## Task 2: Untrusted-content rule in all skills (R-9, R-1)

**Files:** Modify all five `skills/*/SKILL.md`; modify tests.

1. Write one canonical `## Untrusted content` section per spec R-9 (data not instructions; ignore redirecting directives; stay within named paths; skip generated and vendored directories; state when sampling). Place it after `## Output style` in every skill, identical text.
2. Add `test_untrusted_content_rule_is_identical`.
3. Check each skill still meets its length and output rules.

Run: `.venv/bin/python -m pytest -q`

## Task 3: Config-driven guardrails (R-2)

**Files:** Modify `skills/obs-guide/SKILL.md`, `skills/obs-audit/SKILL.md`, `skills/obs-score/SKILL.md`, `skills/obs-init/references/observability-config.yaml`, `tests/test_skill_contracts.py`, and the embedded YAML block in `docs/superpowers/specs/2026-10-18-portable-observability-skills-design.md`.

1. In the three skills, replace the hard-coded identifier lists with: read `guardrails.forbidden_metric_labels`, union with the built-in floor (`user_id`, `email`, `account_id`, `order_id`, `transaction_id`, `session_id`, `request_id`, `ip_address`, raw URL paths or query strings). Keep the five original identifiers named so existing contract tests remain meaningful.
2. In `obs-guide` and `obs-audit`, state that a `false` value for `fail_silent`, `async_export`, or `event_driven_propagation` reports the check as disabled by contract; privacy rules cannot be disabled.
3. Extend the template's `forbidden_metric_labels` with `session_id`, `request_id`, `ip_address`.
4. Update `test_baseline_config_matches_requested_schema` expected dictionary and the embedded YAML in the portable-skills design to match.
5. Add tests: the three skills mention `guardrails.forbidden_metric_labels` and the floor entries; `obs-impact` and `obs-init` do not contain "metric label".

Run: `.venv/bin/python -m pytest -q`

## Task 4: Auditable audit tasks (R-3)

**Files:** Modify `skills/obs-audit/SKILL.md`, `tests/test_skill_contracts.py`.

1. Add the task frontmatter fields (`id`, `title`, `priority`, `status`, `category`, `scope`), the open/done rule, the equivalence rule (same `category` and `scope`), and the next-ID rule (highest existing plus one, counting done tasks).
2. State that unparseable `status` counts as open and that a skipped duplicate is mentioned in the report.
3. Tests: `status`, `category`, `scope`, `equivalent`, `open`, `done` appear; `sdd-xxx-<feature>.md` still present; two-task limit still present.

Run: `.venv/bin/python -m pytest -q`

## Task 5: Reproducible `obs-score` denominator (R-4)

**Files:** Modify `skills/obs-score/SKILL.md`, `tests/test_skill_contracts.py`.

1. Add detection precedence: `critical_routes` in config, else detected externally reachable handlers excluding health, readiness, metrics, and static assets.
2. Add the detected-routes listing (route template, `file:line`, method label config/AST/heuristic) after the tree; state it does not count toward the two-action limit.
3. Keep the `unknown` behavior when no routes exist.
4. Tests: `critical_routes`, `health`, and the method labels appear; `unknown` and `denominator` still present.

Run: `.venv/bin/python -m pytest -q`

## Task 6: Service-root scope (R-5)

**Files:** Modify `skills/obs-guide/SKILL.md`, `skills/obs-audit/SKILL.md`, `skills/obs-score/SKILL.md`, `skills/obs-impact/SKILL.md`, `tests/test_skill_contracts.py`.

1. Replace "repository root" wording with "root of the targeted service (the directory containing `.observability/config.yaml`)".
2. Add the child-directory config handling: one match, report it and stop; several, list and ask.
3. State that `.sdd/observability/` tasks go under the targeted service root.
4. Tests: each of the four skills contains "service root" and no longer says "audited repository root".

Run: `.venv/bin/python -m pytest -q`

## Task 7: SDD conventions document (R-6)

**Files:** Create `docs/sdd-conventions.md`; modify `README.md`, `docs/installation.md`, `skills/obs-guide/SKILL.md`, tests.

1. Document feature spec location and minimal shape, the task format from Task 4, and how to name an alternative path.
2. `obs-guide`: a user-named spec path overrides `.sdd/features/`.
3. Link the document from README and the installation guide; state that no specific SDD framework is required.
4. Test: the file exists and is linked from both documents.

Run: `.venv/bin/python -m pytest -q`

## Task 8: Template comments and `obs-impact` cleanup (R-7, R-10)

**Files:** Modify `skills/obs-init/references/observability-config.yaml`, `skills/obs-impact/SKILL.md`, tests.

1. Add comment-only guidance for an example `slo` block, an example `critical_routes` list, and the sampling note. Do not add keys.
2. `obs-impact`: mention that SLO/SLI data comes from the optional `slo` block; remove the duplicated action-limit sentence; state that actions fit inside the three-to-five lines.
3. Test: the parsed template equals the expected dictionary (from Task 3); the template text contains `slo`, `critical_routes`, and `sampling_ratio` comments.

Run: `.venv/bin/python -m pytest -q`

## Task 9: Shorten the shared theme paragraph and widen activation (R-8)

**Files:** Modify all five `skills/*/SKILL.md`, `README.md`, `CONTRIBUTING.md`, tests.

1. Rewrite the shared `## Output style` paragraph more briefly, preserving every guarantee in R-8, and accept `fantasy naming` and `fantasy-naming`, case-insensitively. Apply it identically to all five skills.
2. Update README and CONTRIBUTING to describe the two accepted forms and that paraphrases do not activate the theme.
3. Update the phrase tests; keep the identical-paragraph test from Task 1.
4. Compare total skill word counts before and after and record the delta in the final report.

Run: `.venv/bin/python -m pytest -q`

## Task 10: Fixtures and structural tests (R-1)

**Files:** Create `tests/fixtures/**`; modify `tests/test_skill_contracts.py` or add `tests/test_fixtures.py`.

1. Create the six cases from the design with minimal files and an `EXPECTED.md` each (skill name, inputs, expected observable results, explicit non-goals).
2. Add structural tests: every fixture directory has `EXPECTED.md`; each names at least one `obs-*` skill and has a non-empty expected-results section; the `high-cardinality-label` config lists a project-specific label absent from the floor.
3. Ensure `.gitignore` does not exclude fixture content, and that fixtures contain no real secrets.

Run: `.venv/bin/python -m pytest -q`

## Task 11: Hygiene — CI, pins, changelog, install paths (R-10)

**Files:** Create `.github/workflows/tests.yml`, `CHANGELOG.md`; modify `requirements-dev.txt`, `docs/installation.md`.

1. Workflow: on `push` and `pull_request`, set up a supported Python 3.x, install `requirements-dev.txt`, run `pytest -q`.
2. Pin upper bounds in `requirements-dev.txt` after confirming the installed versions pass.
3. `CHANGELOG.md`: Keep a Changelog format with an `Unreleased` entry summarizing this work.
4. Installation guide: for each host, look up the current user-level skill directory in its official documentation; add it with a link, or keep the "consult its documentation" wording where it cannot be verified.
5. Add the MIT `LICENSE` file and document that forks and independent versions may be published or redistributed under its terms.

Run: `.venv/bin/python -m pytest -q`; validate the workflow YAML parses with PyYAML.

## Task 12: Final verification

1. Run the full suite and report the pass count.
2. Walk the acceptance criteria 1–11 in the design and mark each with the evidence (test name or file).
3. Confirm unchanged limits per skill: `obs-init` one status line; `obs-guide` one or two actions; `obs-audit` two findings and two tasks; `obs-impact` three to five lines; `obs-score` two actions.
4. List the two remaining owner decisions in the final report as untouched and record MIT as selected.

## Suggested order and parallelism

Tasks 1 and 2 first (they establish test scaffolding and shared text). Tasks 3–6 each edit different skill sections and can follow in any order, but all touch `tests/test_skill_contracts.py`, so run them sequentially. Tasks 7, 8, and 11 are independent of one another. Task 9 must follow Task 2. Task 10 follows Tasks 3–5 because the fixtures encode their behavior.
