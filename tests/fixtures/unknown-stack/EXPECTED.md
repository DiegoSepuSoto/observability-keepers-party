# Expected behavior: unknown-stack

Applies to `obs-init`.

Inputs: no supported manifest or workspace declaration establishes a language stack or service identity.

Expected results: `obs-init` reports the stack as `unknown` and does not infer a service name from source files or directory names. If the service boundary is otherwise clear, it may initialize from the bundled template with `service: unnamed-service`.

Non-goal: do not guess based on file extensions.
