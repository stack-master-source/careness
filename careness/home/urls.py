from django.urls import path
from django.conf.urls import url

from .views import (
    cards_edit_view,
    cards_view,
    create_card_view,
    dash_view,
    home_view,
    sub_card_view,
)

urlpatterns = [
    url(r"^$", home_view, name="home"),
    url("^cards/$", cards_view, name="cards"),
    url("^sub_cards/$", sub_card_view, name="sub_cards"),
    url("^cards/edit/$", cards_edit_view, name="cards_edit"),
    url("^cards/create/$", create_card_view, name="cards_create"),
    url("^dash/$", dash_view, name="dash"),
]
