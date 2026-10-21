# Expected behavior: requests-without-users

Applies to `obs-impact`.

Inputs: an observation window includes request counts and 5xx counts, but no distinct affected-user identities or matching population denominator.

Expected results: report request impact only and mark user impact as `unavailable`. Do not derive an affected-user percentage from request counts.

Non-goal: do not expose raw request fields or add personal identifiers to the fixture.
