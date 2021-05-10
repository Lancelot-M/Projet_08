"""Testing views file"""

import pytest
from django.test import Client
from swap_food.models import Aliment, Nutriment
from pytest_django.asserts import assertTemplateUsed, assertContains


class TestSwapFoodViews():
    """test views's file"""
    client = Client()

    @pytest.fixture
    def miam(self, db):
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

    def test_home(self, client):
        """test home page view"""
        response = client.get('')
        assert response.status_code == 200
        assertTemplateUsed(response, 'swap_food/home.html')

    def test_research(self, client, db, miam):
        """test search food view"""
        response = client.get('/research/', {'search_food': 'nutella'})
        assert response.status_code == 200
        assertTemplateUsed(response, 'swap_food/results.html')
        assertContains(response, "nutella")
        assert response.context["aliments_list"]

    def test_research_donotexist(self, client, db, miam):
        """test search food view"""
        response = client.get('/research/', {
                              'search_food': 'produit_imaginaire'})
        assert response.status_code == 200
        assertTemplateUsed(response, 'swap_food/results.html')

    def test_info(self, client, db, miam):
        """test info food page"""
        response = client.get('/info/nutella/')
        assert response.status_code == 200
        assertTemplateUsed('swap_food/info.html')
        assertContains(response, "PROTEINES : 0.1")

    def test_mention(self, client):
        """test mention food"""
        response = client.get('/mentions/')
        assert response.status_code == 200
        assertTemplateUsed(response, "swap_food/mentions.html")
