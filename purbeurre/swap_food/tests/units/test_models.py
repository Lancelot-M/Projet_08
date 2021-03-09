from swap_food.models import Aliment, Nutriment, Nutrition


class Test_Aliment():
    """ test model Aliment"""

    def test_add_nutriment(self, db):
        """test add_nutriment method"""
        nutriment = Nutriment(name="carbohydrates_100g")
        nutriment.save()
        nutriment = Nutriment(name="fat_100g")
        nutriment.save()
        aliment = Aliment(name="chocolate")
        aliment.save()
        nutriments_data = {
            "carbohydrates_100g": "10",
            "fat_100g": "3",
        }
        aliment.add_nutriment(nutriments_data)
        chocolate_glucide = Nutrition.objects.get(aliment__name="chocolate",
                                                  nutriment__name="carbohydra"
                                                  "tes_100g")
        assert chocolate_glucide.value == "10"
