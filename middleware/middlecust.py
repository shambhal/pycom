

from .cust import CustClass
from django.urls import reverse
    
class CustMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.customer = CustClass(request.user)
        return self.get_response(request)
