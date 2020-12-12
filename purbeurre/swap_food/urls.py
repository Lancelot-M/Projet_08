from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('info/<str:aliment_name>/', views.info, name='info'),
]