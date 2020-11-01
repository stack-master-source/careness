from django.urls import path

from .views import (
    cards_edit_view,
    cards_view,
    create_card_view,
    dash_view,
    home_view,
    sub_card_view,
)

urlpatterns = [
    path("", home_view, name="home"),
    path("cards/", cards_view, name="cards"),
    path("sub_cards/", sub_card_view, name="sub_cards"),
    path("cards/edit/", cards_edit_view, name="cards_edit"),
    path("cards/create/", create_card_view, name="cards_create"),
    path("dash/", dash_view, name="dash"),
]
