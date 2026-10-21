@app.post("/payments/{payment_id}")
def create_payment(payment_id: str):
    return create(payment_id)


@app.get("/internal/debug")
def debug():
    return {"ok": True}
