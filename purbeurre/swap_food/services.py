"""File with subfunction from views.py"""

from swap_food.models import Nutrition

class Services():
    """Services class for swap_food views."""
    @staticmethod
    def info_aliment(aliment):
        """Format nutrition value to list ["color", value]"""
        query = Nutrition.objects.filter(aliment=aliment)
        nutrition_data = {}
        for query_element in query:
            nutrition_data[query_element.nutriment.name] = query_element.value
        name_fr = {
            "carbohydrates_100g": "glucides",
            "fat_100g": "lipides",
            "proteins_100g": "proteines",
            "salt_100g": "sel",
        }
        for key, value in name_fr.items():
            if key in nutrition_data:
                nutrition_data[value] = nutrition_data.pop(key)
        for key, value in nutrition_data.items():
            if float(value) <= 1:
                nutrition_data[key] = ["bg-success", value]
            elif float(value) >= 10:
                nutrition_data[key] = ["bg-danger", value]
            else:
                nutrition_data[key] = ["bg-yellow", value]
        return nutrition_data
