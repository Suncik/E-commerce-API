from rest_framework.views import exception_handler


class ApplicationError(Exception):
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


def custom_exception_handler(exc, context):
    if isinstance(exc, ApplicationError):
        from rest_framework.response import Response
        return Response(
            {"error": True, "message": exc.message, "details": None},
            status=exc.status_code,
        )

    response = exception_handler(exc, context)
    if response is not None:
        response.data = {"error": True, "message": str(exc), "details": response.data}
    return response