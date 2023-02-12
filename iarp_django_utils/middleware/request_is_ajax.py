class AddRequestIsAjax(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        def is_ajax():
            return any(
                [
                    request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest",
                    request.content_type == "application/json",
                    request.META.get("HTTP_ACCEPT") == "application/json",
                    request.META.get('HTTP_HX_REQUEST'),
                ]
            )

        request.is_ajax = is_ajax

        return self.get_response(request)
