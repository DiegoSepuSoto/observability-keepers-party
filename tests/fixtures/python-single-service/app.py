from fastapi import FastAPI
import logging

app = FastAPI()
logger = logging.getLogger(__name__)

@app.get("/invoices/{invoice_id}")
def get_invoice(invoice_id: str):
    logger.info("invoice requested", extra={"route": "/invoices/{invoice_id}"})
    return {"id": invoice_id}
