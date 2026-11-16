# Expected behavior: playbook-debugging-redirect

Applies to `obs-playbook`.

Inputs: the request "figure out which region is causing the checkout latency spike".

Expected results: the skill identifies a debugging request, redirects to `obs-investigate`, and produces no playbook.

Non-goal: do not prescribe debugging steps or promise incident resolution.
