# Install the Observability Skills

The canonical packages live under `skills/`. These folders are not auto-discovered from that source path; copy or link the complete folder into the host's native skill directory. Keep `SKILL.md` and any `references/` files together. You can install one skill or all five.

The skills do not require a specific SDD framework. See [the SDD conventions](sdd-conventions.md) for feature-spec and audit-task formats.

## OpenCode

For a project-local install, use `.opencode/skills/<skill-name>/SKILL.md`:

```sh
mkdir -p .opencode/skills/obs-init
cp -R skills/obs-init/. .opencode/skills/obs-init/
```

Replace `obs-init` with another folder under `skills/` to install a different skill. To link the canonical package instead of copying it:

```sh
mkdir -p .opencode/skills
ln -s "$PWD/skills/obs-init" .opencode/skills/obs-init
```

OpenCode activation is prompt-based through the agent's skill support. For example, run a prompt such as:

```sh
opencode run "Use the obs-init skill to initialize observability in this repository."
```

This is an agent prompt, not a universal `opencode run <skill-name>` command alias.

For user-level installation paths, consult [OpenCode's current skills documentation](https://opencode.ai/docs/skills/).

## Claude Code

For a project-local install, use `.claude/skills/<skill-name>/SKILL.md`:

```sh
mkdir -p .claude/skills/obs-init
cp -R skills/obs-init/. .claude/skills/obs-init/
```

Replace `obs-init` to install another skill. In a Claude Code session, invoke a skill by its slash name, for example `/obs-init`. Claude Code also supports user-level skills; consult its current documentation for the user directory if you want the skills available across projects.

See [Claude Code's skills documentation](https://docs.anthropic.com/en/docs/claude-code/skills) for current user-level installation details.

## Codex

For a project-local install, use `.agents/skills/<skill-name>/SKILL.md`:

```sh
mkdir -p .agents/skills/obs-init
cp -R skills/obs-init/. .agents/skills/obs-init/
```

Replace `obs-init` to install another skill. In a Codex task, explicitly request a skill by name, for example `$obs-init`, or describe the task and let Codex select a matching skill. Codex also supports user-level skill directories; consult its current documentation for the user directory if you want the skills available across projects.

See the [Codex skills guide](https://developers.openai.com/codex/skills-and-plugins/) for current discovery and activation behavior.

## Updating and removing

When updating a copied skill, copy the contents of its canonical folder into the matching installed folder so bundled references stay in sync. Remove only the corresponding installed skill directory when uninstalling; do not remove `.observability/config.yaml` or SDD artifacts created in the audited project.

Activation syntax differs by host. These skills share their instructions and artifacts, but there is no single invocation command that works unchanged across all three tools.
