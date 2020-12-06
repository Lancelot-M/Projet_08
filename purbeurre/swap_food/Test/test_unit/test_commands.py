import pytest
from swap_food.management.commands.commands import DumpsCategories, ImportData
from swap_food.models import Aliment, Additive

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

    def test_categories_without_childs(self, monkeypatch, object_test):
        """test function eponym"""
        def mock_get_taxonomies(self):
            """mock get_taxonomies"""
            pass
        def mock_reverse_taxonomies(self):
            """mock reverse_taxonomies()"""
            pass
        monkeypatch.setattr(DumpsCategories, 'get_taxonomies', mock_get_taxonomies)
        monkeypatch.setattr(DumpsCategories, 'reverse_taxonomies', mock_reverse_taxonomies)
        object_test.categories = ["en:banana", "en:chocolat", "en:ice-cream"]
        object_test.taxonomies = {
            "parent-1": ["child-A", "child-B"],
            "en:ice-cream": ["child-E"],
            "parent-3": ["child-A", "child-B", "child-C"]
        }
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
            self.data_temp = [
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
        monkeypatch.setattr(ImportData, "get_category", mock_get_category)
        error = object_test.make_import(9, 10)
        aliment = Aliment.objects.get(name="aliment_a")
        additive = Additive.objects.filter(aliment__name="aliment_b")
        additive = [el.name for el in additive]
        assert aliment.name == "aliment_a"
        assert aliment.image == "path/to/url"
        assert aliment.category == "category_name"
        assert aliment.allergens == "-- unknow --"
        assert aliment.ingredients == "-- unknow --"
        assert aliment.store == "-- unknow --"
        assert aliment.image_s == "-- unknow --"
        assert aliment.grade_food == "a"
        assert error == "END OF MAKE IMPORT"
        assert additive == ["en:e300", "en:e330", "en:e666","en:d444"]

    def test_make_import_errorin_category(self, monkeypatch, object_test):
        """test if get_category return an error"""
        def mock_get_category(self, category_name):
            """mock get_category"""
            return "PRODUCT ERROR IN THIS CATEGORY"
        monkeypatch.setattr(ImportData, "get_category", mock_get_category)
        error = object_test.make_import(0, 1)
        assert error == "ERROR WITH sweetened-beverages"

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

    def test_category_product_error(self, monkeypatch, object_test):
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

    def test_category_status_error(self, monkeypatch, object_test):
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

    def test_filter_category(self, object_test):
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

    def test_filter_tags(self, object_test):
        """test function eponym"""
        object_test.data = [
            {
                "product_name_fr": "is_valid\n",
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
                "product_name_fr": "is_valid",
                "image_url": "is_valid",
                "nutrition_grade_fr": "",
                "nutriments": "",
                "key_usless_1": "is_valid",
                "key_usless_2": "is_valid",
                "category": "category_name"
            }
        ]
        object_test.filter_tags()
        assert object_test.data_temp == [
            {
                "product_name_fr": "is_valid",
                "image_url": "is_valid",
                "nutrition_grade_fr": "o",
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
                "nutrition_grade_fr": "a",
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
                "nutrition_grade_fr": "",
                "nutriments": {},
                "category": "category_name",
                "image_small_url": "-- unknow --",
                "stores": "-- unknow --",
                "ingredients_text": "-- unknow --",
                "additives_tags": [],
                "allergens": "-- unknow --",
            }
        ]