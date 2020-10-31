from django.urls import path

from .views import home_view, cards_view

urlpatterns = [
    path("", home_view, name="home"),
    path("cards/", cards_view, name="cards")
]
