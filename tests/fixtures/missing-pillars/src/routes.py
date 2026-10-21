from framework import app


@app.get("/reports")
def reports():
    return {"items": []}
