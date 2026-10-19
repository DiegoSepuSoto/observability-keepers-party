# Expected behavior: monorepo-ambiguous

Applies to `obs-init`.

Inputs: two independent service manifests with different declared names.

Expected results: `obs-init` stops before creating a root contract and lists both service names and manifest paths, then asks which service to initialize.

Non-goal: do not choose a service by directory order.
