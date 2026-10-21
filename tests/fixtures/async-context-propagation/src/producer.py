from opentelemetry.propagate import inject


def publish(body, headers):
    inject(headers)
    broker.send(body, headers=headers)
