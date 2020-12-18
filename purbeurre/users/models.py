from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
    aliments_saved = models.ManyToManyField('swap_food.Aliment')