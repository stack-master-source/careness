import json
import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render

logger = logging.getLogger(__name__)


def login_view(request, template="sign_in/login.html"):
    if request.method == "GET":
        return render(request, template)

    elif request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        user = authenticate(username=data["username"], password=data["password"])

        if user is not None:
            login(request, user)
            return redirect("home")
        return JsonResponse({"success": 0})


def register_view(request, template="sign_in/register.html"):
    if request.method == "GET":
        return render(request, template)

    elif request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        user = User.objects.create_user(
            data["username"], data["email"], data["password"]
        )
        try:
            user.save()
            user_ = authenticate(username=data["username"], password=data["password"])
            login(request, user_)
            return redirect("home")
        except Exception as e_info:
            logger.error(e_info)
            return JsonResponse({"success": 0})


def logout_view(request):
    logout(request)  # logout from system
    return redirect("login")
