from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.template import loader
from .models import Aliments

def index(request):
    template = loader.get_template("swap_food/index.html")
    return HttpResponse(template.render(request=request))

def search(request):
    if request.method == 'GET':
        research = Aliments.objects.get(name=request.GET["search_food"])
        aliments_list = Aliments.objects.filter(category=research.category)
        template = loader.get_template("swap_food/results.html")
        context = {
            "aliments_list": aliments_list,
            "research": research,
        }
        return HttpResponse(template.render(context=context, request=request))