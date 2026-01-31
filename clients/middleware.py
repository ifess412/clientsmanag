# error handling middleware
from django.core.exceptions import PermissionDenied
from django.shortcuts import render

import threading


class PermissionDeniedErrorHandler:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        # This is the method that responsible for the safe-exception handling
        if isinstance(exception, PermissionDenied):
            return render(
                request=request,
                template_name="clients/403.html",
                status=403
            )
        return None
    


_request_local = threading.local()

class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _request_local.request = request
        response = self.get_response(request)
        return response

def get_current_request():
    return getattr(_request_local, 'request', None)