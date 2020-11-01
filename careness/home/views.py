import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render

from .models import Cards, Cities, SubCards


def _dd(content):
    raise Exception(content)


def home_view(request, template="home/home.html"):
    if request.method == "GET":
        return render(request, template)


@login_required
def create_card_view(request, template="home/create_card.html"):
    if request.method == "GET":
        cities = Cities.objects.all()  # noqa
        serialized_cities = json.loads(serializers.serialize("json", cities))

        return render(request, template, {"cities": serialized_cities})


def dash_view(request, template="home/admin.html"):
    if request.method == "GET":
        cards = Cards.objects.filter(user__pk=request.user.id)  # noqa
        cities = Cities.objects.all()  # noqa
        sub_cards = SubCards.objects.filter(user__pk=request.user.id)  # noqa

        serialized_sub_cards = json.loads(serializers.serialize("json", sub_cards))
        serialized_cards = json.loads(serializers.serialize("json", cards))
        serialized_cities = json.loads(serializers.serialize("json", cities))

        for card in serialized_cards:
            for city in serialized_cities:
                if card["fields"]["city"] == city["pk"]:
                    card["fields"]["city"] = city["fields"]["name"]

        for sub_card in serialized_sub_cards:
            for city in serialized_cities:
                if sub_card["fields"]["city"] == city["pk"]:
                    sub_card["fields"]["city"] = city["fields"]["name"]

        return render(
            request,
            template,
            {
                "cards": serialized_cards,
                "sub_cards": serialized_sub_cards,
                "cities": serialized_cities,
            },
        )


@login_required
def cards_view(request, template="home/cards.html"):
    if request.method == "GET":
        cities = Cities.objects.all()  # noqa
        cards = Cards.objects.all()  # noqa
        sub_cards = SubCards.objects.all()  # noqa
        users = User.objects.all()

        serialized_cities = json.loads(serializers.serialize("json", cities))
        serialized_users = json.loads(serializers.serialize("json", users))
        serialized_cards = json.loads(serializers.serialize("json", cards))
        serialized_sub_cards = json.loads(serializers.serialize("json", sub_cards))

        for card in serialized_cards:
            card["fields"]["sub_cards"] = []

            for sub_card in serialized_sub_cards:
                if card["pk"] == sub_card["fields"]["card"]:
                    card["fields"]["sub_cards"].append(sub_card)

            for user in serialized_users:
                if card["fields"]["user"] == user["pk"]:
                    card["fields"]["user"] = user

            for city in serialized_cities:
                if card["fields"]["city"] == city["pk"]:
                    card["fields"]["city"] = city

        return render(
            request,
            template,
            {
                "cities": serialized_cities,
                "cards": serialized_cards,
            },
        )

    elif request.method == "POST":
        city_id = request.POST.get("city")
        tel_number = request.POST.get("tel_number")
        comment = request.POST.get("comment")
        prod_link = request.POST.get("product_link")
        prod_name = request.POST.get("product_name")
        count = request.POST.get("product_count")
        date = request.POST.get("date")

        try:
            cards = Cards(
                user_id=request.user.id,
                city_id=city_id,
                name=prod_name,
                product_link=prod_link,
                tel_number=tel_number,
                count=count,
                comment=comment,
                date=date,
            )
            cards.save()
            return JsonResponse({"success": 1})
        except Exception as e_info:
            print(e_info)
            return JsonResponse({"success": 0})


def cards_edit_view(request):
    if request.method == "POST":
        method = request.POST.get("type")
        card_id = request.POST.get("card_id")

        try:
            card = Cards.objects.get(pk=card_id, user__pk=request.user.id)  # noqa
        except Cards.DoesNotExist:  # noqa
            return JsonResponse({"success": -1})

        if not card:
            return JsonResponse({"success": -1})

        if method == "update":
            product_link = request.POST.get("product_link")
            count = request.POST.get("count")
            city = request.POST.get("city")
            name = request.POST.get("product_name")
            comment = request.POST.get("comment")
            date = request.POST.get("date")
            tel_number = request.POST.get("tel_number")

            city_ = Cities.objects.get(pk=city)  # noqa

            card.product_link = product_link
            card.count = count
            card.city = city_
            card.comment = comment
            card.name = name
            card.tel_number = tel_number
            card.date = date

            try:
                card.save()
                return JsonResponse({"success": 1})
            except Exception as e_info:
                print(e_info)
                return JsonResponse({"success": 0})

        elif method == "delete":
            try:
                card.delete()
                return JsonResponse({"success": 1})
            except Exception as e_info:
                print(e_info)
                return JsonResponse({"success": 0})

    elif request.method == "GET":
        card_id = request.GET.get("card_id")
        card = Cards.objects.filter(pk=card_id, user__pk=request.user.id)  # noqa

        if len(card) > 0:
            card_serialized = json.loads(serializers.serialize("json", card))
            return JsonResponse({"success": 1, "data": card_serialized})

        return JsonResponse({"success": -1, "data": []})


def sub_card_view(request):
    if request.method == "GET":
        method = request.GET.get("type")
        card_id = request.GET.get("card_id")

        if method == "dash":
            sub_cards = SubCards.objects.filter(  # noqa
                card__pk=card_id, user__pk=request.user.id
            )
            sub_cards_serialized = json.loads(serializers.serialize("json", sub_cards))
            return JsonResponse({"success": 1, "data": sub_cards_serialized})

        elif method == "page":
            users = User.objects.all()
            serialized_users = json.loads(serializers.serialize("json", users))
            sub_cards = SubCards.objects.filter(card__pk=card_id)  # noqa
            sub_cards_serialized = json.loads(serializers.serialize("json", sub_cards))

            for sub_card in sub_cards_serialized:
                for user in serialized_users:
                    if sub_card["fields"]["user"] == user["pk"]:
                        sub_card["fields"]["user"] = user

            return JsonResponse({"success": 1, "data": sub_cards_serialized})

        return JsonResponse({"success": -1, "data": []})

    elif request.method == "POST":
        method = request.POST.get("type")

        if method == "create":
            card_id = request.POST.get("card_id")
            city_id = request.POST.get("city_id")
            prod_link = request.POST.get("product_link")
            count = request.POST.get("count")
            product_name = request.POST.get("product_name")
            comment = request.POST.get("comment")
            date = request.POST.get("date")

            try:
                sub_card = SubCards(
                    card_id=card_id,
                    user_id=request.user.id,
                    city_id=city_id,
                    product_link=prod_link,
                    count=count,
                    name=product_name,
                    comment=comment,
                    date=date,
                )
                sub_card.save()
                return JsonResponse({"success": 1})
            except Exception as e_info:
                print(e_info)
                return JsonResponse({"success": 0})

        elif method == "update":
            sub_card_id = request.POST.get("sub_card_id")
            prod_link = request.POST.get("product_link")
            product_name = request.POST.get("product_name")
            count = request.POST.get("count")
            comment = request.POST.get("comment")
            date = request.POST.get("date")
            city = request.POST.get("city")

            city_ = Cities.objects.get(pk=city)  # noqa

            sub_card = SubCards.objects.get(
                pk=sub_card_id, user__pk=request.user.id
            )  # noqa
            sub_card.product_link = prod_link
            sub_card.city = city_
            sub_card.count = count
            sub_card.comment = comment
            sub_card.date = date
            sub_card.name = product_name

            try:
                sub_card.save()
                return JsonResponse({"success": 1})
            except Exception as e_info:
                print(e_info)
                return JsonResponse({"success": 0})

        elif method == "delete":
            sub_card_id = request.POST.get("sub_card_id")
            sub_card = SubCards.objects.filter(pk=sub_card_id)  # noqa

            try:
                sub_card.delete()
                return JsonResponse({"success": 1})
            except Exception as e_info:
                print(e_info)
                return JsonResponse({"success": 0})
