"""models for users application"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from swap_food.models import Aliment

class MyUser(AbstractUser):
    """users model"""
    aliments_saved = models.ManyToManyField('swap_food.Aliment')

    def save_aliment(self, aliment_name):
        """save aliment_name for the user instance"""
        aliment = Aliment.objects.get(name=aliment_name)
        self.aliments_saved.add(aliment)
