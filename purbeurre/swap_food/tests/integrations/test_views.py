"""Testing views file"""

from django.test import Client
from swap_food.models import Aliment, Nutriment
from pytest_django.asserts import assertTemplateUsed, assertContains

client = Client()


def test_home(client):
    """test home page view"""
    response = client.get('')
    assert response.status_code == 200
    assertTemplateUsed(response, 'swap_food/home.html')


def test_research(client, db):
    """test search food view"""
    aliment = Aliment(name="nutella")
    aliment.save()
    nutriment = Nutriment(name="carbohydrates_100g")
    nutriment.save()
    nutriment = Nutriment(name="fat_100g")
    nutriment.save()
    nutriment = Nutriment(name="proteins_100g")
    nutriment.save()
    nutriments_data = {
        "carbohydrates_100g": "20",
        "fat_100g": "9",
        "proteins_100g": "0.1",
    }
    aliment.add_nutriment(nutriments_data)
    response = client.get('/research/', {'search_food': 'nutella'})
    assert response.status_code == 200
    assertTemplateUsed(response, 'swap_food/results.html')
    assertContains(response, "nutella")


def test_info(client, db):
    """test info food page"""
    aliment = Aliment(name="nutella")
    aliment.save()
    nutriment = Nutriment(name="carbohydrates_100g")
    nutriment.save()
    nutriment = Nutriment(name="fat_100g")
    nutriment.save()
    nutriment = Nutriment(name="proteins_100g")
    nutriment.save()
    nutriments_data = {
        "carbohydrates_100g": "20",
        "fat_100g": "9",
        "proteins_100g": "0.1",
    }
    aliment.add_nutriment(nutriments_data)
    response = client.get('/info/nutella/')
    assert response.status_code == 200
    assertTemplateUsed('swap_food/info.html')
    assertContains(response, "PROTEINES : 0.1")


def test_mention(client):
    """test mention food"""
    response = client.get('/mentions/')
    assert response.status_code == 200
    assertTemplateUsed(response, "swap_food/mentions.html")
