# Expected behavior: sli-cause-based-request

Applies to `obs-sli`.

Inputs: the request "the checkout service is healthy when CPU stays under 70% and queue depth under 100".

Expected results: the skill asks for a user-perspective rephrasing, names a symptom-based alternative such as the proportion of checkout requests that succeed, and generates no `slo:` block. If the user insists after one explanation, it declines and states the reason.

Non-goal: do not write to `.observability/config.yaml`.
