from opentelemetry.propagate import extract


def consume(message):
    carrier = {"traceparent": message.headers.get("traceparent")}
    context = extract(carrier)
    return process(message.body, context=context)
