from flask import json, Response, request, url_for


class ApiResult:
    def __init__(self, value, status=200, next_page: int = None):
        self.value = value
        self.status = status
        self.next_page = next_page

    def to_response(self) -> Response:
        rv = Response(json.dumps(self.value), status=self.status, mimetype="application/json")
        if self.next_page is not None:
            link = url_for(request.url, self.next_page)
            rv.headers["Link"] = f'<{link}>; rel="next"'
        return rv


class ApiException(Exception):
    def __init__(self, message: str, status=400):
        super().__init__(message)
        self.message = message
        self.status = status

    def to_result(self) -> ApiResult:
        return ApiResult({"error": self.message}, self.status)
