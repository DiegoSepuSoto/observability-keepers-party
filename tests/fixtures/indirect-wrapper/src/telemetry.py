def traced(operation):
    def decorate(handler):
        def wrapped(*args, **kwargs):
            with tracer.start_as_current_span(operation):
                return handler(*args, **kwargs)
        return wrapped
    return decorate
