"""File testing models.py"""

from swap_food.models import Aliment
from users.models import MyUser


def test_save_aliment(db):
    """User's method"""
    choco = Aliment(name="chocolate")
    choco.save()
    user = MyUser.objects.create_user("user_test", "user_test@email.com",
                                      "password")
    user.save_aliment("chocolate")
    assert user.aliments_pref.filter(name="chocolate")


def test_rate_aliment(db):
    """User's method"""
    choco = Aliment(name="chocolate")
    choco.save()
    user = MyUser.objects.create_user("user_test", "user_test@email.com",
                                      "password")
    data_send = {
        "aliment": "chocolate",
        "rate": 1
    }
    user.rate_aliment(data_send)
    assert user.aliments_rate.filter(name="chocolate")
