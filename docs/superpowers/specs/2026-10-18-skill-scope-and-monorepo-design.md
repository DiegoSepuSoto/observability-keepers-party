# Observability Skill Scope and Monorepo Design

## Goal

Clarify service selection in `obs-init` and make each observability skill carry only the instructions needed for its responsibility. Keep the skills portable, self-contained, and consistent with the existing observability contract.

This change supplements the portable-skills design. Where that design requires every skill to repeat every telemetry guardrail, this specification narrows the requirement to the skills whose work uses that guardrail.

## Service selection in `obs-init`

`obs-init` must not choose a service arbitrarily when repository manifests identify multiple independent services.

- If relevant manifests identify one unambiguous service, initialize the contract as before, using a reliable declared service name when available and `unnamed-service` when it is not.
- If relevant manifests identify multiple independent services, or conflicting names make the target unclear, stop before creating `.observability/config.yaml`. Report the candidate names and manifest paths, then ask the user which service to initialize or ask them to run the skill from the selected service root.
- Manifests that agree on one service identity do not create ambiguity.
- An existing `.observability/config.yaml` remains untouched and continues to take precedence over detection.
- Keep the successful initialization response to one concise English status line. For ambiguity, use one concise English status line that names the ambiguity and candidates.

## Responsibility-based skill instructions

Retain detailed implementation guardrails where they affect instrumentation decisions:

- `obs-guide` gives instrumentation guidance, so it retains low-cardinality labels, sensitive-data handling, asynchronous fail-silent export, W3C message propagation, and source-evidence limits.
- `obs-audit` checks instrumentation, so it retains the full source-verification and telemetry guardrail checks.
- `obs-score` scores route-level source evidence. It retains static-versus-runtime evidence rules, low-cardinality metric criteria, and output privacy. It does not present export behavior or message propagation as part of the route score unless those are explicitly made part of the score's scope.
- `obs-init` creates the contract from its bundled template. The template remains the authoritative source for telemetry defaults; onboarding instructions focus on safe service detection and contract creation instead of repeating source-audit procedures.
- `obs-impact` summarizes verified evidence for stakeholders. It retains evidence limits, unavailable-value rules, and privacy protections, while omitting implementation guidance such as `BatchSpanProcessor`, metric-label construction, and `traceparent` propagation.

## Validation changes

Update package-contract tests to match these responsibilities:

- Continue checking that all five skills have valid, matching frontmatter.
- Require full instrumentation guardrails only from `obs-guide` and `obs-audit`.
- Check that `obs-init` handles ambiguous service candidates and relies on the bundled template for contract defaults.
- Check that `obs-score` preserves its static evidence, low-cardinality metric, and privacy requirements without requiring unrelated export or queue instructions.
- Check that `obs-impact` preserves evidence integrity, unavailable estimates, and privacy requirements without requiring instrumentation implementation details.

The tests remain static package-contract checks; they do not prove that an agent follows the instructions at runtime.

## Out of scope

- Changing the baseline YAML schema or values.
- Editing application source code or creating observability task artifacts.
- Adding host-specific behavior, runtime dependencies, or an LLM execution harness.
- Changing the five skills' output language, action limits, or core purpose.

## Acceptance criteria

1. `obs-init` stops before writing when manifest evidence presents multiple plausible services and reports the candidates and their manifest paths.
2. `obs-init` still creates the baseline contract for one unambiguous service and preserves an existing contract.
3. Detailed instrumentation guardrails live only in the skills that need them; `obs-impact` remains focused on supported business claims and privacy.
4. Tests enforce each skill's relevant contract rather than requiring every guardrail in every skill.
5. The existing baseline template, skill portability, and static-evidence limitations remain intact.
