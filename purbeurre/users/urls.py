from django.urls import path, include
from .views import register, profil, aliments

urlpatterns = [
    path('accounts/', include("django.contrib.auth.urls")),
    path('register/', register, name="register"),
    path('profil/', profil, name="profil"),
    path('aliments/', aliments, name='aliments'),
]