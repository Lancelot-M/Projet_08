import pytest
from swap_food.management.commands.commands import DumpsCategories, ImportData, DeleteData
from swap_food.models import Aliment, Additive, Nutriment, Nutrition
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
                    "allergens": "-- unknow --",
                    "additives_tags": [
                        "en:e161b",
                        "en:e202",
                        "en:e211"
                    ],
                    "category": "category_name",
                    "image_url": "path/to/url",
                    "product_name_fr": "aliment_a",
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
                    },
                },
                {
                    "additives_tags": [
                        "en:e300",
                        "en:e330",
                        "en:e666",
                        "en:d444"
                    ],
                    "product_name_fr": "aliment_b",
                    "image_url": "is_valid",
                    "nutrition_grade_fr": "o",
                    "nutriments": {},
                    "category": "category_name",
                    "image_small_url": "-- unknow --",
                    "stores": "-- unknow --",
                    "ingredients_text": "-- unknow --",
                    "allergens": "-- unknow --",
                    "image_small_url": "-- unknow --"
                }
            ]
            return "GET SUCCES"
        monkeypatch.setattr(ImportData, "get_category", mock_get_category)
        returned = object_test.make_import(9, 10)

        alim = Aliment.objects.get(name="aliment_a")
        additive_list = [el.name for el in Additive.objects.filter(aliment__name="aliment_b")]
        glucide = Nutriment.objects.get(name="carbohydrates_100g")
        nutriments_list = [element.name for element in alim.nutriments.all()]
        alimenta_glucide = Nutrition.objects.get(aliment=alim, nutriment=glucide)
        assert alim.name == "aliment_a"
        assert returned == "END OF MAKE IMPORT"
        assert additive_list == ["en:e300", "en:e330", "en:e666","en:d444"]
        assert alimenta_glucide.score == "suga"
        assert nutriments_list == ["carbohydrates_100g","energy-kcal_100g","fat_100g",
            "fiber_100g","proteins_100g","salt_100g","sodium_100g","sugars_100g"]

    def test_make_import_category_error(self, monkeypatch, object_test):
        """test fail import cause error in one category """
        def mock_get_category(self, category_name):
            return "PRODUCT ERROR IN THIS CATEGORY"
        monkeypatch.setattr(ImportData, "get_category", mock_get_category)
        result = object_test.make_import(0, 1)
        assert result == "ERROR WITH sweetened-beverages"

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

    def test_get_or_create_additive_already_exist(self, db, object_test):
        a1 = Additive(name="e666")
        a1.save()
        object_test.get_or_create_additive("e666")
        a2 = Additive.objects.all()
        assert len(a2) == 1

    def test_get_or_create_additive_not_exist(self, db, object_test):
        object_test.get_or_create_additive("e666")
        a1 = Additive.objects.all()
        assert a1[0].name == "e666"

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
        result = object_test.get_or_create_aliment(product)
        a1 = Aliment.objects.all()
        assert a1[0].name == "chocolate"
        assert result == None

    def test_make_relation_is_ok(self, db, object_test):
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
        for element in product["additives_tags"]:
            a = Additive(name=element)
            a.save()
        for element in product["nutriments"]:
            a = Nutriment(name=element)
            a.save()
        a = Aliment(allergens=product["allergens"], category=product["category"],
                    image=product["image_url"], name=product["product_name_fr"],
                    grade_food=product["nutrition_grade_fr"], store=product["stores"],
                    ingredients=product["ingredients_text"], image_s=product["image_small_url"])
        a.save()
        object_test.make_relation(product)
        a = Aliment.objects.get(name="chocolate")
        d = Nutriment.objects.get(name="proteins_100g")
        n = Nutrition.objects.get(aliment=a, nutriment=d)
        assert a.category == "category_name"
        assert d.name == "proteins_100g"
        assert n.score == "1"

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
                },
                {
                    "product_name_fr": "is_valid",
                    "image_url": "is_valid",
                    "nutrition_grade_fr": "is_valid",
                    "nutriments": "is_valid",
                    "key_usless_1": "is_valid",
                    "key_usless_2": "is_valid"
                },
                {
                    "product_name_fr": "is_valid",
                    "image_url": "is_valid",
                    "nutrition_grade_fr": "is_valid",
                    "nutriments": "is_valid",
                    "key_usless_1": "is_valid",
                    "key_usless_2": "is_valid"
                },
                {
                    "product_name_fr": "is_valid",
                    "image_url": "is_valid",
                    "nutrition_grade_fr": "is_valid",
                    "nutriments": "is_valid"
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
                    "category": "category_name"
                },
                {
                    "product_name_fr": "is_valid",
                    "image_url": "is_valid",
                    "nutrition_grade_fr": "is_valid",
                    "nutriments": "is_valid",
                    "key_usless_1": "is_valid",
                    "key_usless_2": "is_valid",
                    "category": "category_name"
                },
                {
                    "product_name_fr": "is_valid",
                    "image_url": "is_valid",
                    "nutrition_grade_fr": "is_valid",
                    "nutriments": "is_valid",
                    "key_usless_1": "is_valid",
                    "key_usless_2": "is_valid",
                    "category": "category_name"
                },
                {
                    "product_name_fr": "is_valid",
                    "image_url": "is_valid",
                    "nutrition_grade_fr": "is_valid",
                    "nutriments": "is_valid",
                    "category": "category_name"
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
                "category": "category_name"
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
                "category": "category_name"
            },
            {
                "product_name_fr": "IS_valid",
                "image_url": "is_valid",
                "nutrition_grade_fr": "dd",
                "nutriments": "",
                "key_usless_1": "is_valid",
                "key_usless_2": "is_valid",
                "category": "category_name"
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
                    "energy-kcal_100g": "2",
                    "fat_100g": "2",
                    "fiber_100g": "2"
                },
                "category": "category_name",
                "image_small_url": "-- unknow --",
                "stores": "-- unknow --",
                "ingredients_text": "-- unknow --",
                "additives_tags": [],
                "allergens": "-- unknow --",
            },
            {
                "product_name_fr": "is_valid",
                "image_url": "is_valid",
                "nutrition_grade_fr": "A",
                "nutriments": {
                    "carbohydrates_100g" : "1",
                    "energy-kcal_100g": "1",
                    "fat_100g": "1",
                    "fiber_100g": "1",
                    "proteins_100g": "1",
                    "salt_100g": "1",
                    "sodium_100g": "1",
                    "sugars_100g": "1",
                },
                "category": "category_name",
                "image_small_url": "-- unknow --",
                "stores": "-- unknow --",
                "ingredients_text": "-- unknow --",
                "additives_tags": [],
                "allergens": "-- unknow --",
            },
            {
                "product_name_fr": "is_valid",
                "image_url": "is_valid",
                "nutrition_grade_fr": "DD",
                "nutriments": {},
                "category": "category_name",
                "image_small_url": "-- unknow --",
                "stores": "-- unknow --",
                "ingredients_text": "-- unknow --",
                "additives_tags": [],
                "allergens": "-- unknow --",
            }
        ]

class Test_DeleteData():
    """test cleaning class"""
    def test_clean_all(self, db):
        """test if all tables are deleted"""
        a = Aliment(name='aliment', category="aliment_cat")
        a.save()
        a = Additive(name="e:404")
        a.save()
        object_test = DeleteData()
        object_test.clean_all()
        b = Additive.objects.all().exists()
        c = Aliment.objects.all().exists()
        assert b == False
        assert c == False
