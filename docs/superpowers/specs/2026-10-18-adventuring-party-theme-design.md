# Adventuring Party Voice for Observability Skills: Design

## Goal

Add an optional, lightweight fantasy voice to the five portable observability skills while keeping their current enterprise voice as the default. The optional style uses an adventuring-party theme and remains in English. Technical facts, evidence limits, privacy rules, output formats, and action limits remain authoritative in either style.

## Scope

Update the five canonical skill instructions under `skills/` and the repository documentation that explains their behavior. Do not add a CLI, runtime, host-specific wrapper, theme configuration, or dependency. The repository does not implement a logging runtime or commercial presentation generator, so this change applies to skill responses and their generated text only.

All repository content and skill output remain in English. Remove references to D&D and use the “Adventuring Party” naming. The literal phrase `fantasy naming` is the opt-in signal. A skill uses the themed voice only when that phrase appears in the request invoking the skill. Otherwise, it uses the current enterprise style.

## Design

### Portable activation and shared rule

Each skill remains usable as an independent package. Add the same concise theme contract directly to every `SKILL.md`, followed by only that skill's role mapping. The repeated rule states that enterprise is the default, `fantasy naming` opts into the Adventuring Party voice, outputs stay in English, and metaphors must not replace or alter technical facts. This deliberate duplication avoids a shared-file dependency when a user installs only one skill.

The signal is ordinary request text interpreted by the agent. It is not a CLI argument, persistent setting, or config field. Do not change native skill invocation syntax for OpenCode, Claude Code, or Codex.

### Role mapping and voice

| Skills | Character | Voice and metaphor scope |
| --- | --- | --- |
| `obs-init`, `obs-score` | Cartographer | Careful scout who relies on repository evidence before moving forward. The codebase is the expedition terrain; `.observability/config.yaml` is the expedition map; the scorecard describes the party's readiness. |
| `obs-guide` | Sentinel Guard | Calm protector beside the developer. Cardinality controls are a protective shield; asynchronous, fail-silent export is a protective aura; spans are lines of guard. |
| `obs-audit` | Spectral Inquisitor | Incisive and evidence-led. AST inspection is an oracle for source truth; verified gaps are cracks; generated `.sdd/observability/*.md` tasks may be framed as quest scrolls. |
| `obs-impact` | Troubadour | Concise translator for stakeholders. Product stakeholders are the council; RED metrics and SLOs describe the realm's state; customer impact describes protection of its inhabitants. |

When the theme is active, a skill may add at most one brief character-framed sentence or label before its technical content. Keep the persona restrained and specific to the skill. Do not add a second layer of decorative prose.

### Technical fidelity and existing contracts

The themed voice decorates presentation only. Preserve exact command names, error codes, file paths, OpenTelemetry attribute names, filenames, and measured values. Keep evidence, uncertainty, and limitations explicit. Never turn a static result into a runtime claim or state an impact that available evidence does not support. Express errors and missing evidence directly, without dramatization.

All existing per-skill output contracts remain in force in both modes:

- `obs-init` keeps its concise one-line status or ambiguity response and does not overwrite an existing contract.
- `obs-score` keeps its compact ASCII scorecard, static-evidence framing, and maximum of two priority actions.
- `obs-guide` keeps focused, feature-specific guidance and no more than one or two priority actions; it does not edit application source.
- `obs-audit` keeps its evidence requirements, maximum of two prioritized findings, and maximum of two executable SDD tasks.
- `obs-impact` keeps its three-to-five-line business summary, privacy limits, evidence requirements, and maximum of two actions.

The character framing must fit within these limits. For `obs-impact`, it counts as part of the existing three-to-five lines rather than adding a line.

### Documentation and validation

Update README and contributing guidance to describe the default style, the exact textual opt-in, the role mapping, and the fact that no CLI or shared runtime is introduced. Preserve the existing portability and installation model.

Validate the change through a manual contract review of all five skill instructions and documentation. Confirm that the shared rule matches exactly, every role mapping is present, the opt-in is explicit, and each existing output limit and technical guardrail remains intact. This design does not add a test suite or runtime validation.

## Alternatives considered

1. **Repeat a short rule in each skill (selected).** Each skill remains self-contained and portable. The rule is duplicated, so its wording must be kept synchronized.
2. **Load one shared theme guide.** This reduces duplicated text but makes each standalone skill depend on an additional reference being installed and read.
3. **Add host or CLI theme configuration.** This could provide structured configuration but would broaden the project beyond its portable-skill architecture and introduce host-specific behavior or runtime work.

## Acceptance criteria

1. Enterprise style remains the default for all five skills.
2. The literal request signal `fantasy naming` activates the Adventuring Party voice for the invoked skill; no CLI, config field, or runtime is added.
3. Every skill can be installed alone and includes the same concise shared theme rule.
4. Each skill uses its assigned character only when the theme is active, with no more than one brief persona-framed sentence or label.
5. All content remains in English, and documentation uses “Adventuring Party” without D&D references.
6. Technical identifiers, evidence quality, privacy constraints, output formats, and action limits remain unchanged in both modes.
7. README and contributing guidance explain activation and portability without implying a custom CLI.

## Risks and mitigations

- **The repeated rule can drift.** Keep one canonical paragraph copied identically into every skill and review all five together when it changes.
- **The theme can crowd out useful evidence.** Cap persona framing at one brief sentence or label and retain every existing output limit.
- **A phrase can be mistaken for a CLI option.** Document it only as natural-language request text and do not show it as a shell command.
