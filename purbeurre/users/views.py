from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
from users.forms import CustomUserCreationForm
from users.models import MyUser
from django.http import Http404

def register(request):
    if request.method == "GET":
        return render(
            request, "users/register.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("home"))

def profil(request):
    if request.method == "GET":
        return render(
            request, "users/profil.html",
        )

def aliments(request):
    if request.user.is_authenticated:
        aliments = request.user.aliments_saved.all()
        return render(
            request, "users/aliments.html",
            {"aliments_list": aliments}
        )
    else:
        raise Http404("YOU ARE NOT LOGGED !")