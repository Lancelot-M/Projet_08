from django.shortcuts import render
from swap_food.models import Aliment, Nutrition
from swap_food.services import Services

def home(request):
    return render(request, "swap_food/home.html")

def research(request):
    if request.method == 'GET':
        try:
            searched_aliment = request.GET["search_food"].lower()
            research = Aliment.objects.get(name=searched_aliment)
            aliments_list = Aliment.objects.filter(category=research.\
                category).order_by("nutrition_grade")[:9]
        except Aliment.DoesNotExist:
            return render(
                request, "swap_food/results.html",
                {"bubble": searched_aliment}
            )
        return render(
            request, "swap_food/results.html",
            {
                "aliments_list": aliments_list,
                "background": research.image,
                "bubble": searched_aliment
            }
        )

def info(request, aliment_name):
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

def mentions(request):
    return render(request, "swap_food/mentions.html")