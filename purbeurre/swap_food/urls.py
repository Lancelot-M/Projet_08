from django.urls import path, include
from . import views


urlpatterns = [
    path('home/', views.home, name='home'),
    path('research/', views.research, name='research'),
    path('info/<str:aliment_name>/', views.info, name='info'),
]