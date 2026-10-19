# Expected behavior: node-single-service

Applies to `obs-init`, `obs-score`, and `obs-audit`.

Inputs: one Node.js service with a contract and two request routes.

Expected results: `obs-init` recognizes `shop-api` and does not overwrite the existing contract. `obs-score` includes `/orders/{orderId}` and `/checkout` in the critical-route denominator, with source evidence for the first route and a gap on the second. `obs-audit` may report at most two prioritized gaps and cites source lines.

Non-goal: static evidence does not claim runtime coverage.
