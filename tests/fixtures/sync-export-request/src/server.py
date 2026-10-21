from opentelemetry.sdk.trace import SimpleSpanProcessor

provider.add_span_processor(SimpleSpanProcessor(exporter))


def handle_request(request):
    with tracer.start_as_current_span("checkout"):
        return process(request)
