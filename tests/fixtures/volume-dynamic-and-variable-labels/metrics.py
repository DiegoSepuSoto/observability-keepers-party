requests = meter.create_counter("payments.requests")
latency = meter.create_histogram("payments.latency")

def record(route_template, region, tenant_code, status_class):
    requests.add(1, {"http.route": route_template, "cloud.region": region,
                     "tenant_code": tenant_code, "status_class": status_class})
    latency.record(0.2, {"http.route": route_template})
