import requests
import json
import copy
from swap_food.config import KEEPED_DATA, NUTRIMENTS_LIST
from swap_food.models import Aliment, Nutriment
from django.core.exceptions import ObjectDoesNotExist


class DumpsCategories():
    """class who generate a file with all usable categories"""
    def __init__(self):
        self.categories = []
        self.taxonomies = {}
        self.without_child = []

    def make_dump(self):
        """main class function"""
        self.get_all_categories()
        self.categories_without_childs()
        with open("swap_food/management/commands/categories.json", "w") as f:
            f.write(json.dumps(self.without_child, indent=4, sort_keys=True,
                               ensure_ascii=False))

    def get_all_categories(self):
        """make_dump: get all "en:" categories"""
        url = "https://fr-en.openfoodfacts.org/categories.json"
        request = requests.get(url)
        data = request.json()
        if "tags" in data:
            for element in data["tags"]:
                if element["id"][0:3] == "en:" and element["id"][3].isalpha():
                    self.categories.append(element["id"])

    def categories_without_childs(self):
        """make_dump: keep only categories who have no category child"""
        self.get_taxonomies()
        self.reverse_taxonomies()
        for category in self.categories:
            if category not in self.taxonomies:
                self.without_child.append(category[3:])

    def get_taxonomies(self):
        """categories_without_childs: get and filter taxonomies data"""
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
        """categories_without_childs: make tree structure from taxonomies"""
        reversed_taxonomy = {}
        for child, parents in self.taxonomies.items():
            for parent in parents["parents"]:
                if parent in reversed_taxonomy:
                    reversed_taxonomy[parent].append(child)
                else:
                    reversed_taxonomy[parent] = [child]
        self.taxonomies = reversed_taxonomy


class ImportData():
    """get products from off and add them in database"""
    def __init__(self):
        self.data = {}
        self.products_to_import = []

    def make_import(self, start, end):
        """main class function"""
        with open("swap_food/management/commands/categories.json", "r") as f:
            all_categories = json.load(f)
        for category in all_categories[start:end]:
            result = self.get_category(category)
            if type(result) is str:
                if result == "PRODUCT ERROR IN THIS CATEGORY":
                    print(f"PRODUCT ERROR IN THIS CATEGORY : {category}")
                else:
                    return result
        print("----- DOWNLOADED -------------")
        for product in self.products_to_import:
            if self.create_product(product) == "ERROR WITH DB":
                return "ERROR WITH DB"
        return "END OF MAKE IMPORT"

    def get_category(self, category_name):
        """make_import: get products data about one category"""
        url = "https://fr-en.openfoodfacts.org/category/{}.json"
        request = requests.get(url.format(category_name))
        if request.status_code == 200:
            self.data = request.json()
            self.filter_category(category_name)
            if type(self.data) is str:
                return self.data
            self.filter_tags()
            self.data = {}
            return None
        else:
            self.data = f"{category_name} ---> {request.status_code}"
            return self.data

    def create_product(self, product):
        """make_import: main product creation function"""
        if self.get_or_create_aliment(product) == "ALREADY EXIST":
            print("PRODUCT ALREADY EXIST")
            return None
        for key in product["nutriments"].keys():
            self.get_or_create_nutriment(key)
        if self.make_relation(product) == "ERROR WITH DB":
            return "ERROR WITH DB"

    def get_or_create_nutriment(self, nutriment):
        """create_product: add nutriment in db if doesn't exist"""
        try:
            a = Nutriment.objects.get(name=nutriment)
        except ObjectDoesNotExist:
            a = Nutriment(name=nutriment)
            a.save()

    def get_or_create_aliment(self, product):
        """create_product: add aliment to db if doesn't exist"""
        try:
            a = Aliment.objects.get(name=product["product_name_fr"])
            return "ALREADY EXIST"
        except ObjectDoesNotExist:
            a = Aliment(category=product["category"], source=product["url"],
                        image=product["image_url"],
                        name=product["product_name_fr"],
                        nutrition_grade=product["nutrition_grade_fr"])
            a.save()
            return None

    def make_relation(self, product):
        """create_product: relation aliment/nutriment throught nutrition"""
        try:
            a = Aliment.objects.get(name=product["product_name_fr"])
            a.add_nutriment(product["nutriments"])
        except ObjectDoesNotExist:
            return "ERROR WITH DB"

    def filter_category(self, category_name):
        """get_category: remove product without required tags"""
        if "products" not in self.data:
            self.data = "PRODUCT ERROR IN THIS CATEGORY"
            return
        self.data = self.data["products"]

        def checker(product):
            for tag in ["product_name_fr", "image_url", "url",
                        "nutrition_grade_fr", "nutriments"]:
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
        """get_category: clean usless tags and standardize values"""
        for element in self.data:
            product = {}
            for tag in KEEPED_DATA:
                if tag in element:
                    if tag == "nutriments":
                        nutri_dict = {}
                        for nutriment in NUTRIMENTS_LIST:
                            if nutriment in element[tag]:
                                nutri_dict[nutriment] = str(element[tag]
                                                            [nutriment])
                            else:
                                nutri_dict[nutriment] = "?"
                        product[tag] = nutri_dict
                    elif tag == "nutrition_grade_fr":
                        product[tag] = element[tag].upper()
                    elif tag == "product_name_fr":
                        product[tag] = element[tag].replace("\n", "").lower()
                    else:
                        product[tag] = element[tag]
                else:
                    product[tag] = "unknow"
            self.products_to_import.append(product)


class DeleteData():
    """Clean all datas from db swap_app"""
    def clean_all(self):
        Aliment.objects.all().delete()
        Nutriment.objects.all().delete()
