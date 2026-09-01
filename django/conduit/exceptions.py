from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated, AuthenticationFailed

def token_missing_exception_handler(exc, context):
    # get default error response
    response = exception_handler(exc, context)

    # check if theres missing token or invalid token
    if isinstance(exc, (NotAuthenticated, AuthenticationFailed)) and response:
        # structure expected by API contract
        data = {
            "errors": {
                "token": ["is missing"]
            }
        }
        return Response(data, status=response.status_code)

    return response