import requests, json, copy
from swap_food.config import KEEPED_DATA, NUTRIMENTS_LIST
from swap_food.models import Aliment, Additive
from django.core.exceptions import ObjectDoesNotExist

class DumpsCategories():
    def __init__(self):
        self.categories = []
        self.taxonomies = {}
        self.without_child = []

    def make_dump(self):
        self.get_all_categories()
        self.categories_without_childs()
        with open("swap_food/management/commands/categories.json", "w") as f:
            f.write(json.dumps(self.without_child, indent=4, sort_keys=True, ensure_ascii=False))

    def get_all_categories(self):
        url = "https://fr-en.openfoodfacts.org/categories.json"
        request = requests.get(url)
        data = request.json()
        if "tags" in data:
            for element in data["tags"]:
                if element["id"][0:3] == "en:" and element["id"][3].isalpha():
                    self.categories.append(element["id"])

    def categories_without_childs(self):
        self.get_taxonomies()
        self.reverse_taxonomies()
        for category in self.categories:
            if category not in self.taxonomies:
                self.without_child.append(category[3:])

    def get_taxonomies(self):
        url = "https://fr-en.openfoodfacts.org/data/taxonomies/categories.json"
        request = requests.get(url)
        self.taxonomies = request.json()
        dict_cpy = self.taxonomies.copy()
        for category_name in dict_cpy.keys():
            if category_name[0:3] == "en:" and category_name[3].isalpha():
                continue
            else:
                self.taxonomies.pop(category_name)
        dict_cpy = copy.deepcopy(self.taxonomies)
        for category_name, taxonomy in dict_cpy.items():
            if "parents" not in taxonomy:
                self.taxonomies.pop(category_name)
                continue
            for key in taxonomy.keys():
                if key != "name" and key != "parents":
                    self.taxonomies[category_name].pop(key)

    def reverse_taxonomies(self):
        reversed_taxonomy = {}
        for child, parents in self.taxonomies.items():
            for parent in parents["parents"]:
                if parent in reversed_taxonomy:
                    reversed_taxonomy[parent].append(child)
                else:
                    reversed_taxonomy[parent] = [child]
        self.taxonomies = reversed_taxonomy

class ImportData():
    def __init__(self):
        self.data = {}
        self.data_temp = []
        self.products_to_import = []

    def get_or_create_additive(self, additive):
        try:
            a = Additive.objects.get(name=additive)
        except ObjectDoesNotExist:
            a = Additive(name=additive)
            a.save()

    def create_aliment(self, product):
        for element in product["additives_tags"]:
                self.get_or_create_additive(element)
        try:
            p = Aliment(allergens=product["allergens"], category=product["category"],
                    image=product["image_url"], name=product["product_name_fr"],
                    grade_food=product["nutrition_grade_fr"], store=product["stores"],
                    ingredients=product["ingredients_text"], image_s=product["image_small_url"])
            p.save()
            for count, element in enumerate(product["additives_tags"]):
                self.data[str(count)] = Additive.objects.get(name=element)
            for value in self.data.values():
                p.additives.add(value)
        except:
            return "ERROR WITH DB"

    def make_import(self, start, end):
        with open("swap_food/management/commands/categories.json", "r") as f:
            all_categories = json.load(f)
        for category in all_categories[start:end]:
            if self.get_category(category) == "PRODUCT ERROR IN THIS CATEGORY":
                return f"ERROR WITH {category}"
        for product in self.data_temp:
            if self.create_aliment(product) == "ERROR WITH DB":
                return "ERROR WITH DB"
        return "END OF MAKE IMPORT"

    def get_category(self, category_name):
        """get products data about one category"""
        url = "https://fr-en.openfoodfacts.org/category/{}.json"
        request = requests.get(url.format(category_name))
        if request.status_code == 200:
            self.data = request.json()
            self.filter_category(category_name)
            if type(self.data) is str:
                return self.data
            self.filter_tags()
            self.data = {}
        else:
            return f"{category_name} ---> {request.status_code}"

    def filter_category(self, category_name):
        """remove product without required tags or minimum number"""
        if "products" not in self.data:
            self.data = "PRODUCT ERROR IN THIS CATEGORY"
            return
        self.data = self.data["products"] 
        def checker(product):
            requirement = ["product_name_fr", "image_url", "nutrition_grade_fr", "nutriments"]
            for tag in requirement:
                if tag not in product:
                    return False
                elif product[tag] == "":
                    return False
            return True 
        self.data = list(filter(checker, self.data))
        if len(self.data) <= 3:
            self.data = "PRODUCT ERROR IN THIS CATEGORY"
            return
        for el in self.data:
            el["category"] = category_name

    def filter_tags(self):
        """clean usless tags and standardize values"""
        for element in self.data:
            product = {}
            for tag in KEEPED_DATA:
                if tag in element:
                    if tag == "nutriments":
                        nutri_dict = {}
                        for nutriment in NUTRIMENTS_LIST:
                            if nutriment in element[tag]:
                                nutri_dict[nutriment] = str(element[tag][nutriment])
                        product[tag] = nutri_dict
                    elif tag == "product_name_fr":
                        product[tag] = element[tag].replace("\n", "")
                    else:
                        product[tag] =  element[tag]
                elif tag == "additives_tags":
                    product[tag] = []
                else:
                    product[tag] = "-- unknow --"
            self.data_temp.append(product)

class DeleteData():
    """Clean all datas use carefully."""
    def clean_all(self):
        a = Aliment.objects.all().delete()
        a = Additive.objects.all().delete()