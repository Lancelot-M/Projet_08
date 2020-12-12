from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, Http404
from django.template import loader
from .models import Aliment, Nutrition

def index(request):
    template = loader.get_template("swap_food/index.html")
    return HttpResponse(template.render(request=request))

def search(request):
    if request.method == 'GET':
        try:
            searched_aliment = request.GET["search_food"].lower()
            research = Aliment.objects.get(name=searched_aliment)
            aliments_list = Aliment.objects.filter(category=research.category).order_by("nutrition_grade")[:9]
            template = loader.get_template("swap_food/results.html")
            context = {
                "aliments_list": aliments_list,
                "background": research.image,
                "bubble": searched_aliment
            }
        except Aliment.DoesNotExist:
            template = loader.get_template("swap_food/results.html")
            context = {
                "bubble": searched_aliment
            }
            return HttpResponse(template.render(context=context, request=request))
        return HttpResponse(template.render(context=context, request=request))

def info(request, aliment_name):
    if request.method == 'GET':
        aliment = Aliment.objects.get(name=aliment_name)
        nutrition_value = Nutrition.objects.filter(aliment=aliment)
        new_val = {}
        for element in nutrition_value:
            new_val[element.nutriment.name] = element.value
        nutrition_value = {
            "carbohydrates_100g": "glucides",
            "fat_100g": "lipides",
            "proteins_100g": "proteines",
            "salt_100g": "sel",
        }
        for key1, value1 in nutrition_value.items():
            new_val[value1] = new_val.pop(key1)
        for key, value in new_val.items():
            if float(value) <= 1:
                new_val[key] = ["bg-success", value]
            elif float(value) >= 10:
                new_val[key] = ["bg-danger", value]
            else:
                new_val[key] = ["bg-yellow", value]
        template = loader.get_template("swap_food/info.html")
        context = {
            "background": aliment.image,
            "bubble": aliment.name,
            "aliment": aliment,
            "nutrition": new_val,
        }
        return HttpResponse(template.render(context=context, request=request))