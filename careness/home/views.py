from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from django.contrib.auth.decorators import login_required
from .models import Cards, Cities
from django.core import serializers
import json


def home_view(request):
    return HttpResponse("HELLO")


@login_required
def cards_view(request, template="home/cards.html"):
    if request.method == "GET":
        cities = Cities.objects.all()  # noqa
        serialized_cities = json.loads(serializers.serialize("json", cities))

        return render(request, template, {"cities": serialized_cities})

    elif request.method == "POST":
        city_id = request.POST.get("city")
        prod_link = request.POST.get("product_link")
        prod_count = request.POST.get("product_count")
        date = request.POST.get("date")

        try:
            cards = Cards(
                user_id=request.user.id, city_id=city_id, product_link=prod_link,
                count=prod_count, comment="", date=date
            )
            cards.save()
            return JsonResponse({"success": 1})
        except Exception as e_info:
            print(e_info)
            return JsonResponse({"success": 0})
