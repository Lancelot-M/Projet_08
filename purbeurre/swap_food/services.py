"""File with subfunction from views.py"""

from swap_food.models import Nutrition
from users.models import Rating


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

    @staticmethod
    def make_ratedict(request, aliments_list):
        """Return rating formated for template"""
        rating_dict = {}
        for element in aliments_list:
            try:
                rate = Rating.objects.get(aliment_rate__name=element, myuser_rate=request.user)
            except Rating.DoesNotExist:
                rate = None
            if rate:
                if rate.rating:
                    rate_list = []
                    for i in range(rate.rating):
                        rate_list.append(i)
                    rating_dict[rate.aliment_rate.name] = rate_list
        return rating_dict