"""Testing services file"""

import pytest
from swap_food.models import Aliment, Nutriment
from swap_food.services import Services
from users.models import MyUser
from django.test import Client, RequestFactory


class Test_Services():
    """test services file"""
    client = Client()

    @pytest.fixture
    def create_user(self, db):
        self.factory = RequestFactory()
        self.user = MyUser.objects.create_user(
            "user_test", "user_test@email.com", "password")

    def test_info_aliment(self, db):
        """test the static method info_aliment"""
        aliment = Aliment(name="chocolate")
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
        nutrition_data = Services.info_aliment(aliment)
        assert nutrition_data == {
            "glucides": ["bg-danger", "20"],
            "lipides": ["bg-yellow", "9"],
            "proteines": ["bg-success", "0.1"],
        }

    def test_make_ratedict(self, db, create_user):
        """teste dict creation"""
        request = self.factory.get('/')
        request.user = self.user
        aliments_list = []
        aliment = Aliment(name="chocolate")
        aliment.save()
        aliments_list.append(aliment)
        data_send = {
            "aliment": "chocolate",
            "rate": 1
        }
        request.user.rate_aliment(data_send)
        aliment = Aliment(name="chips")
        aliment.save()
        aliments_list.append(aliment)
        aliment = Aliment(name="pistaches")
        aliment.save()
        aliments_list.append(aliment)

        assert Services.make_ratedict(
            request, aliments_list) == {"chocolate": [0]}
