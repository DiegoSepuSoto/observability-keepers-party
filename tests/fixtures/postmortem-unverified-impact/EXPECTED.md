# Expected behavior: postmortem-unverified-impact

Applies to `obs-postmortem`.

Inputs: an incident summary with start and end times, a customer-report detection, and an unsupported "30% of users" claim; no telemetry.

Expected results: every impact figure is marked `[unverified — telemetry required]`, no user percentage is reported, the root cause is classified `unknown` with the missing telemetry named, timeline gaps are explicit, and action items target observability improvements only.

Non-goal: do not estimate impact or recommend application source changes.
