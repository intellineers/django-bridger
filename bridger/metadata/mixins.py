class BridgerMetadataMixin:
    def __init__(self, view, request, *args, **kwargs):
        self.view = view
        self.request = request
        super().__init__(*args, **kwargs)

    def __iter__(self):
        yield self.key, getattr(self.view, self.method_name)(self.request)
