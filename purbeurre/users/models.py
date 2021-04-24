"""models for users application"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from swap_food.models import Aliment


class MyUser(AbstractUser):
    """users model"""
    aliments_pref = models.ManyToManyField('swap_food.Aliment', related_name="pref", through="Myfood")
    aliments_rate = models.ManyToManyField('swap_food.Aliment', related_name="rate", through="Rating")

    def save_aliment(self, aliment_name):
        """save aliment_name for the user instance"""
        #IF aliments_saved(name=aliment_name) DOESN'T EXIST:
        aliment = Aliment.objects.get(name=aliment_name)
        self.aliments_pref.add(aliment)

    def rate_aliment(self, rating):
        """rate aliment"""
        try:
            rate = Rating.objects.get(aliment_rate__name=rating["aliment"], myuser_rate=self)
            rate.rating = int(rating["rate"])
            rate.save()
        except Rating.DoesNotExist:
            aliment = Aliment.objects.get(name=rating["aliment"])
            rate = Rating(aliment_rate=aliment, myuser_rate=self, rating=rating["rate"])
            rate.save()


class Myfood(models.Model):    
    aliment_pref = models.ForeignKey('swap_food.Aliment', on_delete=models.CASCADE)
    myuser_pref = models.ForeignKey(MyUser, on_delete=models.CASCADE)


class Rating(models.Model):
    aliment_rate = models.ForeignKey('swap_food.Aliment', on_delete=models.CASCADE)
    myuser_rate = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True)
