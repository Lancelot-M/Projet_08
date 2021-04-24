"""Path file"""

from django.urls import path, include
from users.views import register, profil, aliments, saving, rating

urlpatterns = [
    path('accounts/', include("django.contrib.auth.urls")),
    path('register/', register, name="register"),
    path('profil/', profil, name="profil"),
    path('aliments/', aliments, name='aliments'),
    path('saving/', saving, name='saving'),
    path('rating/', rating, name='rating'),
]
