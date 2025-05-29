from django.views.generic import View


class JsonView(View):
    def dispatch(self, request, *args, **kwargs):
        if "json" in request.GET or request.META.get("CONTENT_TYPE") == "application/json":
            return self.json(request=request, *args, **kwargs)
        return super().dispatch(request=request, *args, **kwargs)

    def json(self, request, *args, **kwargs):
        raise NotImplementedError("def json not implemented.")
