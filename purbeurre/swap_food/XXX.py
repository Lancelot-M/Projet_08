import requests, json

class Off_Loader():
    @classmethod
    def call_B(cls):
        products_data = []
        categories_dict = {}
        kepped_tags = [
            "product_name_fr",
            "ingredients_text",
            "image_url",
            "image_small_url",
            "nutrition_grade_fr",
            "additives_tags",
            "allergens",
            "nutriments",
            "stores",
        ]
        nutriments_list = [
            "carbohydrates_100g",
            "energy-kcal_100g",
            "fat_100g",
            "fiber_100g",
            "proteins_100g",
            "salt_100g",
            "sodium_100g",
            "sugars_100g",
        ]
        url = "https://fr-en.openfoodfacts.org/category/iced-coffees.json"
        request_data = requests.get(url)
        request_data = request_data.json()
        for el in request_data["products"]:
            product = {}
            for tag in kepped_tags:
                if tag in el:
                    if tag == "nutriments":
                        nutri_dict = {}
                        for nut in nutriments_list:
                            if nut in el[tag]:
                                nutri_dict[nut] = el[tag][nut]
                        product[tag] = nutri_dict
                    else:
                        product[tag] = el[tag]
            products_data.append(product)
        categories_dict["iced-coffees"] = products_data
        with open("off_categories_X.json", "w") as f:
            f.write(json.dumps(categories_dict, indent=4, sort_keys=True, ensure_ascii=False))
        pass

if __name__ == "__main__" :
    #Off_Loader.call_A()
    Off_Loader.call_B()