"""Path file"""

from django.urls import path
from swap_food import views

urlpatterns = [
    path('', views.home, name='home'),
    path('research/', views.research, name='research'),
    path('info/<str:aliment_name>/', views.info, name='info'),
    path('mentions/', views.mentions, name='mentions'),
]
