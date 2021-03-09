from swap_food.models import Aliment, Nutriment
from swap_food.services import Services


class Test_Services():
    """test view's services file"""
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
