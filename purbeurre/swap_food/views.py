"""File with all swap_food views."""

from django.shortcuts import render
from swap_food.models import Aliment
from users.models import Rating
from swap_food.services import Services


def home(request):
    """Home page of the website"""
    return render(request, "swap_food/home.html")


def research(request):
    """Results of food research page"""
    if request.method == 'GET':
        try:
            searched_aliment = request.GET["search_food"].lower()
            aliment = Aliment.objects.get(name=searched_aliment)
            aliments_list = Aliment.objects.filter(category=aliment.category)\
                .order_by("nutrition_grade")[:9]
        except Aliment.DoesNotExist:
            return render(
                request, "swap_food/results.html",
                {"bubble": searched_aliment}
            )
        if request.user.is_authenticated:
            rating_dict = Services.make_ratedict(request, aliments_list)
        else:
            rating_dict = {}
        return render(
            request, "swap_food/results.html",
            {
                "aliments_list": aliments_list,
                "background": aliment.image,
                "bubble": searched_aliment,
                "rating_dict": rating_dict
            }
        )
    return None


def info(request, aliment_name):
    """Food's detail page."""
    if request.method == 'GET':
        aliment = Aliment.objects.get(name=aliment_name)
        nutrition_data = Services.info_aliment(aliment)
        return render(
            request, "swap_food/info.html",
            {
                "background": aliment.image,
                "bubble": aliment.name,
                "aliment": aliment,
                "nutrition": nutrition_data,
            }
        )
    return None


def mentions(request):
    """Legals mentions"""
    return render(request, "swap_food/mentions.html")
