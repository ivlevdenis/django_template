from rest_framework.views import exception_handler as base_exception_handler


def exception_handler(exc, context):
    response = base_exception_handler(exc, context)
    if response is not None:
        if isinstance(response.data, list):
            return response
        response.data['status_code'] = response.status_code
        if 'detail' in response.data:
            response.data['error'] = response.data['detail']
    return response
