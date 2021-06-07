from django.urls import path

from .views import login_view, logout_view, register_view

urlpatterns = [
    path(r"^login/", login_view, name="login"),
    path(r"^logout/", logout_view, name="logout"),
    path(r"^register/", register_view, name="register"),
]
