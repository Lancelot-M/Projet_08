"""Users's views file"""

import json
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import Http404, HttpResponse
from users.models import Rating
from users.forms import CustomUserCreationForm
from swap_food.services import Services


def register(request):
    """Sign in page"""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("home"))
    return render(
        request, "users/register.html",
        {"form": CustomUserCreationForm}
    )


def profil(request):
    """user's detail page"""
    if request.method == "GET":
        return render(
            request, "users/profil.html",
        )
    return None

def change_mail(request):
    """page for change email"""
    if request.method == "POST":
        request.user.email = request.POST["new_email"]
        request.user.save()
        return render(
        request, "users/profil.html")
    elif request.method == "GET":
        return render(
            request, "users/new_mail.html",
        )
    return None



def aliments(request):
    """user's aliments page"""
    if request.user.is_authenticated:
        user_aliments = request.user.aliments_pref.all()
        rating_dict = Services.make_ratedict(request, user_aliments)
        return render(
            request, "users/aliments.html",
            {
                "aliments_list": user_aliments,
                "rating_dict": rating_dict
            }
        )
    raise Http404("YOU ARE NOT LOGGED !")


def saving(request):
    """saving aliment to favori"""
    if request.method == "POST":
        request.user.save_aliment(request.POST["aliment"])
        aliment_name = json.dumps(request.POST["aliment"])
        return HttpResponse(aliment_name)
    return None


def rating(request):
    """rate for a aliment"""
    if request.method == "POST":
        request.user.rate_aliment(request.POST)
        return HttpResponse("Rate done.")
    return HttpResponse("Rate fail.")
