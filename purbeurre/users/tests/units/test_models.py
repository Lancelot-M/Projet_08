"""File testing models.py"""

import pytest
from swap_food.models import Aliment
from users.models import MyUser

def test_save_aliment(db):
    """Aliment's method"""
    choco = Aliment(name="chocolate")
    choco.save()
    user = MyUser.objects.create_user("user_test", "user_test@email.com", "password")
    user.save_aliment("chocolate")
    assert user.aliments_saved.filter(name="chocolate")
