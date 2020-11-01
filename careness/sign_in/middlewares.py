from django.shortcuts import redirect
from django.urls import reverse


class IsAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated and request.path == reverse("login"):
            return redirect("home")

        if request.user.is_authenticated and request.path == reverse("register"):
            return redirect("home")

        return response
