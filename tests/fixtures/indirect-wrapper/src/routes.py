@traced("GET /catalog")
def catalog():
    return load_catalog()
