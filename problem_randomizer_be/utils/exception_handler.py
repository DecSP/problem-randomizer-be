from rest_framework.views import exception_handler

from problem_randomizer_be.utils.response import CustomResponse


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        return CustomResponse(status_code=response.status_code, message=response.data, headers=response.headers)
    # unhandled exceptions
    return None
