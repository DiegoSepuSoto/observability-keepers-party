const express = require("express");
const { trace, metrics } = require("@opentelemetry/api");
const router = express.Router();
const tracer = trace.getTracer("shop-api");
const requests = metrics.getMeter("shop-api").createCounter("http.requests");

router.get("/orders/:orderId", (req, res) => tracer.startActiveSpan("get-order", (span) => {
  requests.add(1, { "http.route": "/orders/{orderId}", "http.request.method": "GET" });
  console.info({ trace_id: span.spanContext().traceId, route: "/orders/{orderId}" });
  span.end();
  res.sendStatus(200);
}));

router.post("/checkout", (req, res) => res.sendStatus(201));
module.exports = router;
