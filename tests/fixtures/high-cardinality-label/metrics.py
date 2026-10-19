def record(meter, user_id: str, tenant_code: str):
    counter = meter.create_counter("ledger.operations")
    counter.add(1, {"user_id": user_id, "tenant_code": tenant_code})
