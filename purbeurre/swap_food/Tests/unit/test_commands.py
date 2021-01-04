import pytest
from swap_food.management.commands.commands import DumpsCategories, ImportData, DeleteData
from swap_food.models import Aliment, Nutriment, Nutrition
from django.core.exceptions import ObjectDoesNotExist

class Test_Dumps_Command():
    """ class test for DumpsCategories. """

    @pytest.fixture
    def object_test(self):
        """setup who initialize a objet DumpsCategories for test"""
        test = DumpsCategories()
        yield test

    def test_get_all_categories(self, monkeypatch, object_test):
        """ test function eponym"""
        def mock_get_requests(url):
            """ mock requests.get() with a small dict as data """
            class MockRequest:
                """ mock the method of result object """
                def __init__(self, json_data, status_code):
                    self.json_data = json_data
                    self.status_code = status_code
                def json(self):
                    return self.json_data
            data = {
                "count": "something here",
                "tags": [
                    {
                        "url": "path/to/url/exemple",
                        "id": "en:category-valid"
                    },
                    {
                        "url": "path/to/url/exemple",
                        "id": "fr:category-unvalid"
                    },
                    {
                        "url": "path/to/url/exemple",
                        "id": "en:1-category-unvalid"
                    }
                ]
            }
            return MockRequest(data, 200)
        monkeypatch.setattr('requests.get', mock_get_requests)
        object_test.get_all_categories()
        assert object_test.categories == ["en:category-valid"]

    def test_categories_without_child(self, monkeypatch, object_test):
        """test function eponym"""
        def mock_get_taxonomies(self):
            """mock get_taxonomies"""
            pass
        def mock_reverse_taxonomies(self):
            """mock reverse_taxonomies()"""
            self.categories = ["en:banana", "en:chocolat", "en:ice-cream"]
            self.taxonomies = {
                "en:apple": ["child-A", "child-B"],
                "en:ice-cream": ["child-E"],
                "parent-3": ["child-A", "child-B", "child-C"]
            }
        monkeypatch.setattr(DumpsCategories, 'get_taxonomies', mock_get_taxonomies)
        monkeypatch.setattr(DumpsCategories, 'reverse_taxonomies', mock_reverse_taxonomies)
        object_test.categories_without_childs()
        assert object_test.without_child == ["banana", "chocolat"]

    def test_get_taxonomies(self, monkeypatch, object_test):
        """test function eponym"""
        def mock_get_requests(url):
            """ mock requests.get() with a small dict as data """
            class MockRequest:
                """ mock the method of result object """
                def __init__(self, json_data, status_code):
                    self.json_data = json_data
                    self.status_code = status_code
                def json(self):
                    return self.json_data
            data = {
                "bg:cakap": {
                    "name": {
                        "bg": "Cakap"
                    },
                    "origins": {
                        "en": "en:Bulgaria"
                    },
                    "parents": [
                        "en:wines-from-bulgaria"
                    ],
                },
                "en:boiled-oat-flakes": {
                    "name": {
                        "en": "Boiled oat flakes",
                        "fr": "Flocons d'avoine bouillis"
                    },
                    "parents": [
                        "en:rolled-oats"
                    ],
                    "protected_name_file_number": {
                        "en": "PGI-ES-A0128"
                    },
                    "protected_name_type": {
                        "en": "pgi"
                    }
                },
                "en:4444zwieback": {
                    "agribalyse_proxy_food_code": {
                        "en": "7330"
                    },
                    "agribalyse_proxy_food_name": {
                        "en": "Rusk, multigrain",
                        "fr": "Biscotte multic\u00e9r\u00e9ale"
                    }
                }
            }
            return MockRequest(data, 200)
        monkeypatch.setattr('requests.get', mock_get_requests)
        object_test.get_taxonomies()
        assert object_test.taxonomies == {
            "en:boiled-oat-flakes": {
                "name": {
                    "en": "Boiled oat flakes",
                    "fr": "Flocons d'avoine bouillis"
                },
                "parents": [
                    "en:rolled-oats"
                ]
            }
        }

    def test_reverse_taxonomies(self, object_test):
        """test function eponym"""
        object_test.taxonomies = {
            "child-A": {
                "name": {
                    "en": "Boiled oat flakes",
                    "fr": "Flocons d'avoine bouillis"
                },
                "parents": [
                    "parent-1"
                ]
            },
            "child-B": {
                "name": {
                    "en": "Boiled oat flakes",
                    "fr": "Flocons d'avoine bouillis"
                },
                "parents": [
                    "parent-1"
                ]
            },
            "child-C": {
                "name": {
                    "en": "Boiled oat flakes",
                    "fr": "Flocons d'avoine bouillis"
                },
                "parents": [
                    "parent-2"
                ]
            },
        }
        object_test.reverse_taxonomies()
        assert object_test.taxonomies == {
            "parent-1": [
                "child-A",
                "child-B"
            ],
            "parent-2": [
                "child-C"
            ]
        }

class Test_ImportData():
    """test class eponym"""
    @pytest.fixture
    def object_test(self):
        """setup who initialize a objet ImportData for test"""
        test = ImportData()
        yield test

    def test_make_import_succes(self, db, monkeypatch, object_test):
        """test if all works"""
        def mock_get_category(self, category_name):
            self.products_to_import = [
                {
                    "category": "category_name",
                    "url": "path/to/url",
                    "image_url": "url/to/img",
                    "product_name_fr": "aliment_a",
                    "nutrition_grade_fr": "a",
                    "nutriments": {
                        "carbohydrates_100g" : "suga",
                        "fat_100g": "1",
                        "proteins_100g": "1",
                        "salt_100g": "1",



                    },
                },
                {
                    "product_name_fr": "aliment_b",
                    "image_url": "is_valid",
                    "nutrition_grade_fr": "o",
                    "nutriments": {},
                    "category": "category_name",
                    "url": "path/to/url",
                }
            ]
            return None

        monkeypatch.setattr(ImportData, "get_category", mock_get_category)
        returned = object_test.make_import(9, 10)
        alim = Aliment.objects.get(name="aliment_a")
        glucide = Nutriment.objects.get(name="carbohydrates_100g")
        nutriments_list = [element.name for element in alim.nutriments.all()]
        alimenta_glucide = Nutrition.objects.get(aliment=alim, nutriment=glucide)
        
        assert alim.name == "aliment_a"
        assert returned == "END OF MAKE IMPORT"
        assert alimenta_glucide.value == "suga"
        assert nutriments_list == ["carbohydrates_100g","fat_100g",
            "proteins_100g","salt_100g",]

    def test_make_import_category_error(self, monkeypatch, object_test):
        """test fail import cause error in one category """
        def mock_get_category(self, category_name):
            return "sweetened-beverages ---> 404"
        monkeypatch.setattr(ImportData, "get_category", mock_get_category)
        result = object_test.make_import(0, 1)
        assert result == "sweetened-beverages ---> 404"

    def test_make_import_db_error(self, monkeypatch, object_test):
        """test fail import cause db problem"""
        def mock_get_category(self, category_name):
            self.products_to_import = [{"product_dict": "lot_of_value"}]
        def mock_create_product(self, product):
            return "ERROR WITH DB"
        monkeypatch.setattr(ImportData, "get_category", mock_get_category)
        monkeypatch.setattr(ImportData, "create_product", mock_create_product)
        result = object_test.make_import(0, 1)
        assert result == "ERROR WITH DB"

    def test_get_category_succes(self, monkeypatch, object_test):
        """test if off return data from category request"""
        def mock_requests_get(url):
            """mocking function get"""
            class MockRequests:
                def __init__(self, json_data, status_code):
                    self.json_data = json_data
                    self.status_code = status_code
                def json(self):
                    return self.json_data
            data = {
                "count": "18345",
                "page": 1,
                "products": [
                    {
                        "_id": "20702267",
                        "_keywords": [
                            "fromage",
                            "laitier",
                        ],
                        "product_name_fr": "Deluxe Parmigiano Reggiano Fein Gehobelt",
                        "product_quantity": "100",
                        "quantity": "100 g ℮"
                    },
                    {
                        "id": "en:rennet",
                        "percent_estimate": 5,
                        "percent_max": 20,
                        "percent_min": 0,
                        "rank": 5,
                        "text": "présure",
                        "vegan": "maybe",
                        "vegetarian": "maybe"
                    }

                ]
            }
            return MockRequests(data, 200)

        def mock_filter_category(self, category):
            pass
        def mock_filter_tags(self):
            self.products_to_import = ["TEST SUCCES"]
        monkeypatch.setattr(ImportData, "filter_category", mock_filter_category)
        monkeypatch.setattr(ImportData, "filter_tags", mock_filter_tags)
        monkeypatch.setattr('requests.get', mock_requests_get)
        object_test.get_category("category_name")
        assert object_test.products_to_import == ["TEST SUCCES"]

    def test_get_category_product_error(self, monkeypatch, object_test):
        """test if off return no usable product"""
        def mock_get_request(self):
            """mocking requests.get()"""
            class MockRequest:
                """ mock the request object """
                def __init__(self, json_data, status_code):
                    self.json_data = json_data
                    self.status_code = status_code
                def json(self):
                    return self.json_data
            data = { "datas" : "some unusable datas" }
            return MockRequest(data, 200)
        def mock_filter_category(self, category_name):
            """here filter_category return a string cause of error"""
            self.data = "PRODUCT ERROR IN THIS CATEGORY"
        monkeypatch.setattr(ImportData, "filter_category", mock_filter_category)
        monkeypatch.setattr('requests.get', mock_get_request)
        assert object_test.get_category("cheeses") == "PRODUCT ERROR IN THIS CATEGORY"

    def test_get_category_status_error(self, monkeypatch, object_test):
        """test if off got a error status"""
        def mock_get_request(self):
            """mocking requests.get"""
            class MockRequest:
                """mock the request object"""
                def __init__(self, json_data, status_code):
                    self.json_data = json_data
                    self.status_code = status_code
                def json(self):
                    return self.json_data
            data = "nothing cause error"
            return MockRequest(data, 404)
        monkeypatch.setattr("requests.get", mock_get_request)
        assert object_test.get_category("category_with_error") == "category_with_error ---> 404"

    def test_get_or_create_nutriment_already_exist(self, db, object_test):
        a1 = Nutriment(name="sugar")
        a1.save()
        object_test.get_or_create_nutriment("sugar")
        a2 = Nutriment.objects.all()
        assert len(a2) == 1

    def test_get_or_create_nutriment_not_exist(self, db, object_test):
        object_test.get_or_create_nutriment("sugar")
        a1 = Nutriment.objects.all()
        assert a1[0].name == "sugar"

    def test_get_or_create_aliment_already_exist(self, db, object_test):
        product = {
            "allergens": "-- unknow --",
            "additives_tags": [
                "en:e161b",
                "en:e202",
                "en:e211"
            ],
            "category": "category_name",
            "image_url": "path/to/url",
            "product_name_fr": "chocolate",
            "nutrition_grade_fr": "a",
            "stores": "-- unknow --",
            "ingredients_text": "-- unknow --",
            "image_small_url": "-- unknow --",
            "nutriments": {
                "carbohydrates_100g" : "suga",
                "energy-kcal_100g": "1",
                "fat_100g": "1",
                "fiber_100g": "1",
                "proteins_100g": "1",
                "salt_100g": "1",
                "sodium_100g": "1",
                "sugars_100g": "1",
            }
        }
        a1 = Aliment(name="chocolate")
        a1.save()
        result = object_test.get_or_create_aliment(product)
        a2 = Aliment.objects.all()
        assert len(a2) == 1
        assert result == "ALREADY EXIST"

    def test_get_or_create_aliment_not_exist(self, db, object_test):
        product = {
            "category": "category_name",
            "image_url": "path/to/url",
            "url": "product/off/url",
            "product_name_fr": "chocolate",
            "nutrition_grade_fr": "a",
            "nutriments": {
                "carbohydrates_100g" : "suga",
                "energy-kcal_100g": "1",
                "fat_100g": "1",
                "fiber_100g": "1",
                "proteins_100g": "1",
                "salt_100g": "1",
                "sodium_100g": "1",
                "sugars_100g": "1",
            }
        }
        result = object_test.get_or_create_aliment(product)
        a = Aliment.objects.get(category="category_name")
        assert a.name == "chocolate"
        assert result == None

    def test_make_relation_is_ok(self, db, monkeypatch, object_test):
        
        def mock_add_nutriment(self, nutriments_data):
            """make link between aliment and nutriment"""
            aliment = Aliment.objects.get(name="chocolate")
            nutriments_data = {
                "carbohydrates_100g" : "suga",
                "fat_100g": "1",
                "proteins_100g": "1",
                "salt_100g": "0",
            }
            for key, value in nutriments_data.items():
                nutriment = Nutriment.objects.get(name=key)
                nutrition = Nutrition(aliment=aliment, nutriment=nutriment, value=value)
                nutrition.save()

        product = {
            "category": "category_name",
            "image_url": "path/to/url",
            "url": "url/off/to/product",
            "product_name_fr": "chocolate",
            "nutrition_grade_fr": "a",
            "nutriments": {
                "carbohydrates_100g" : "suga",
                "fat_100g": "1",
                "proteins_100g": "1",
                "salt_100g": "0",
            }
        }
        for element in product["nutriments"]:
            nutriment = Nutriment(name=element)
            nutriment.save()
        aliment = Aliment(category=product["category"], source=product["url"],
                    image=product["image_url"], name=product["product_name_fr"],
                    nutrition_grade=product["nutrition_grade_fr"])
        aliment.save()
        returned_value = object_test.make_relation(product)
        
        aliment = Aliment.objects.get(name="chocolate")
        nutriment = Nutriment.objects.get(name="proteins_100g")
        nutrition = Nutrition.objects.get(aliment=aliment, nutriment=nutriment)
        assert aliment.category == "category_name"
        assert nutriment.name == "proteins_100g"
        assert nutrition.value == "1"
        assert returned_value == None

    def test_make_relation_got_exception(self, db, object_test):
        product = {
            "allergens": "-- unknow --",
            "additives_tags": [
                "en:e161b",
                "en:e202",
                "en:e211"
            ],
            "category": "category_name",
            "image_url": "path/to/url",
            "product_name_fr": "chocolate",
            "nutrition_grade_fr": "a",
            "stores": "-- unknow --",
            "ingredients_text": "-- unknow --",
            "image_small_url": "-- unknow --",
            "nutriments": {
                "carbohydrates_100g" : "suga",
                "energy-kcal_100g": "1",
                "fat_100g": "1",
                "fiber_100g": "1",
                "proteins_100g": "1",
                "salt_100g": "1",
                "sodium_100g": "1",
                "sugars_100g": "1",
            }
        }
        result = object_test.make_relation(product)
        assert result == "ERROR WITH DB"

    def test_filter_category_is_ok(self, object_test):
        """test function eponym"""
        object_test.data = {
            "key1": "",
            "key2": "",
            "products": [
                {
                    "product_name_fr": "is_valid",
                    "image_url": "is_valid",
                    "nutrition_grade_fr": "is_valid",
                    "nutriments": "is_valid",
                    "key_usless_1": "is_valid",
                    "key_usless_2": "is_valid",
                    "url": "is_valid",
                },
                {
                    "image_url": "not_valid",
                    "nutrition_grade_fr": "not_valid",
                    "nutriments": "not_valid"
                },
                {
                    "product_name_fr": "",
                    "image_url": "not_valid",
                    "nutrition_grade_fr": "not_valid",
                    "nutriments": "not_valid",
                    "url": "not_valid",
                },
                {
                    "nutrition_grade_fr": "not_valid",
                    "nutriments": "not_valid",
                    "key_usless_1": "not_valid",
                    "key_usless_2": "not_valid"
                },
                {
                    "product_name_fr": "is_valid",
                    "image_url": "is_valid",
                    "nutrition_grade_fr": "is_valid",
                    "nutriments": "is_valid",
                    "key_usless_1": "is_valid",
                    "key_usless_2": "is_valid",
                    "url": "is_valid",
                },
                {
                    "product_name_fr": "is_valid",
                    "image_url": "is_valid",
                    "nutrition_grade_fr": "is_valid",
                    "nutriments": "is_valid",
                    "key_usless_1": "is_valid",
                    "key_usless_2": "is_valid",
                    "url": "is_valid",
                },
                {
                    "product_name_fr": "is_valid",
                    "image_url": "is_valid",
                    "nutrition_grade_fr": "is_valid",
                    "nutriments": "is_valid",
                    "url": "is_valid",
                }
            ]
        }
        object_test.filter_category("category_name")
        assert object_test.data == [
                {
                    "product_name_fr": "is_valid",
                    "image_url": "is_valid",
                    "nutrition_grade_fr": "is_valid",
                    "nutriments": "is_valid",
                    "key_usless_1": "is_valid",
                    "key_usless_2": "is_valid",
                    "category": "category_name",
                    "url": "is_valid",
                },
                {
                    "product_name_fr": "is_valid",
                    "image_url": "is_valid",
                    "nutrition_grade_fr": "is_valid",
                    "nutriments": "is_valid",
                    "key_usless_1": "is_valid",
                    "key_usless_2": "is_valid",
                    "category": "category_name",
                    "url": "is_valid",
                },
                {
                    "product_name_fr": "is_valid",
                    "image_url": "is_valid",
                    "nutrition_grade_fr": "is_valid",
                    "nutriments": "is_valid",
                    "key_usless_1": "is_valid",
                    "key_usless_2": "is_valid",
                    "category": "category_name",
                    "url": "is_valid",
                },
                {
                    "product_name_fr": "is_valid",
                    "image_url": "is_valid",
                    "nutrition_grade_fr": "is_valid",
                    "nutriments": "is_valid",
                    "category": "category_name",
                    "url": "is_valid",
                }
            ]

    def test_filter_category_no_data(self, object_test):
        object_test.data = {
            "key1": "",
            "key2": "",
            "no_products_key": "??"
        }
        object_test.filter_category("category_with_problem")
        assert object_test.data == "PRODUCT ERROR IN THIS CATEGORY"

    def test_filter_category_few_products(self, object_test):
        object_test.data = {
            "key1": "",
            "key2": "",
            "products": [
                {
                    "product_name_fr": "is_valid",
                    "image_url": "is_valid",
                    "nutrition_grade_fr": "is_valid",
                    "nutriments": "is_valid",
                    "key_usless_1": "is_valid",
                    "key_usless_2": "is_valid"
                },
                {
                    "image_url": "not_valid",
                    "nutrition_grade_fr": "not_valid",
                    "nutriments": "not_valid"
                },
                {
                    "product_name_fr": "",
                    "image_url": "not_valid",
                    "nutrition_grade_fr": "not_valid",
                    "nutriments": "not_valid"
                },
                {
                    "nutrition_grade_fr": "not_valid",
                    "nutriments": "not_valid",
                    "key_usless_1": "not_valid",
                    "key_usless_2": "not_valid"
                }
            ]
        }
        object_test.filter_category("not_enought_products")
        assert object_test.data == "PRODUCT ERROR IN THIS CATEGORY"

    def test_filter_tags(self, object_test):
        """test function eponym"""
        object_test.data = [
            {
                "product_name_fr": "IS_VALID\n",
                "image_url": "is_valid",
                "nutrition_grade_fr": "o",
                "nutriments": {
                    "carbohydrates_100g": "2",
                    "energy-kcal_100g": "2",
                    "fat_100g": "2",
                    "fiber_100g": "2",
                    "nutriment_unvalid": "666",
                    "nutriments_unvlid": 999
                },
                "key_usless_1": "is_valid",
                "key_usless_2": "is_valid",
                "category": "category_name",
                "url": "product/url",
            },
            {
                "product_name_fr": "is_valid\n",
                "image_url": "is_valid",
                "nutrition_grade_fr": "a",
                "nutriments": {
                    "carbohydrates_100g" : 1,
                    "energy-kcal_100g": 1,
                    "fat_100g": 1,
                    "fiber_100g": 1,
                    "proteins_100g": 1,
                    "salt_100g": 1,
                    "sodium_100g": 1,
                    "sugars_100g": 1,
                },
                "category": "category_name",
                "url": "product/url",
            },
            {
                "product_name_fr": "IS_valid",
                "image_url": "is_valid",
                "nutrition_grade_fr": "d",
                "nutriments": "",
                "key_usless_1": "is_valid",
                "key_usless_2": "is_valid",
                "category": "category_name",
                "url": "product/url",
            }
        ]
        object_test.filter_tags()
        assert object_test.products_to_import == [
            {
                "product_name_fr": "is_valid",
                "image_url": "is_valid",
                "nutrition_grade_fr": "O",
                "nutriments": {
                    "carbohydrates_100g": "2",
                    "fat_100g": "2",
                    "proteins_100g": "?",
                    "salt_100g": "?",
                },
                "category": "category_name",
                "url": "product/url",
            },
            {
                "product_name_fr": "is_valid",
                "image_url": "is_valid",
                "nutrition_grade_fr": "A",
                "nutriments": {
                    "carbohydrates_100g" : "1",
                    "fat_100g": "1",
                    "proteins_100g": "1",
                    "salt_100g": "1",
                },
                "category": "category_name",
                "url": "product/url",
            },
            {
                "product_name_fr": "is_valid",
                "nutrition_grade_fr": "D",
                "image_url": "is_valid",
                "nutriments": {
                    "carbohydrates_100g" : "?",
                    "fat_100g": "?",
                    "proteins_100g": "?",
                    "salt_100g": "?",
                },
                "category": "category_name",
                "url": "product/url",
            },
        ]

class Test_DeleteData():
    """test cleaning class"""
    def test_clean_all(self, db):
        """test if all tables are deleted"""
        aliment = Aliment(name='aliment', category="aliment_cat")
        aliment.save()
        nutriment = Nutriment(name="nutriment_name")
        nutriment.save()
        nutrition = Nutrition(aliment=aliment, nutriment=nutriment, value="something")
        nutrition.save()
        object_test = DeleteData()

        object_test.clean_all()

        aliment = Aliment.objects.all().exists()
        nutriment = Nutriment.objects.all().exists()
        nutrition = Nutrition.objects.all().exists()

        assert aliment == False
        assert nutriment == False
        assert nutrition == False