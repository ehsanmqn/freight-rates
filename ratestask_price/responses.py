from rest_framework import status

from rest_framework.response import Response


def send_http_response(code, message):
    return Response({
        "code": code,
        "message": "{}".format(message),
        "result": []
    }, status=code)
