# SDD Conventions

These skills do not require a specific spec-driven development framework. They use simple Markdown artifacts and can work with a repository's existing conventions.

## Feature specifications

`obs-guide` looks for the active feature specification under `.sdd/features/` by default. A spec needs only a Markdown title and a description of the behavior being built; no frontmatter or mandated schema is required. If the user names a spec path in the request, that path takes precedence over `.sdd/features/`.

## Observability audit tasks

`obs-audit` writes tasks under `.sdd/observability/` in the targeted service root. Each task is named `sdd-XXX-<feature>.md` and begins with YAML frontmatter containing:

```yaml
id: "001"
title: "Add trace context to payment processing"
priority: high
status: open
category: propagation
scope: "src/payments/consumer.py"
```

`id` is the three-digit sequence from the filename. `priority` is `high` or `medium`; `status` is `open` or `done`; `category` is `cardinality`, `export`, `propagation`, `coverage`, or `data-safety`; and `scope` identifies the file or route targeted by the finding. A task with `status: open` is open. Missing or unparseable status is treated as open. Tasks with the same category and scope are equivalent while open, so `obs-audit` does not create another equivalent open task. New IDs are one greater than the highest existing sequence, including done tasks.

## Using another directory

To use a different location, name the spec or task directory in the request, for example: “Use `architecture/specs/checkout.md` as the feature spec” or “Write audit tasks under `engineering/observability/`.”
