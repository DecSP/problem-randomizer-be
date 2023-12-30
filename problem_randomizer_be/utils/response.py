from rest_framework.response import Response


class CustomResponse:
    def __init__(self, status_code, message, data):
        return Response(status=status_code, data={"statusCode": status_code, "message": message, "data": data})
