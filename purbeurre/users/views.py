"""Users's views file"""

import json
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import Http404, HttpResponse
from users.forms import CustomUserCreationForm


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


def aliments(request):
    """user's aliments page"""
    if request.user.is_authenticated:
        user_aliments = request.user.aliments_saved.all()
        return render(
            request, "users/aliments.html",
            {"aliments_list": user_aliments}
        )
    raise Http404("YOU ARE NOT LOGGED !")


def saving(request):
    """saving aliment to favori"""
    if request.method == "POST":
        request.user.save_aliment(request.POST["aliment"])
        aliment_name = json.dumps(request.POST["aliment"])
        return HttpResponse(aliment_name)
    return None
