"""models for swap_food application"""

from django.db import models

class Nutriment(models.Model):
    """nutriments model"""
    name = models.CharField(max_length=200, unique=True)
    def __str__(self):
        return self.name

class Aliment(models.Model):
    """aliments model"""
    nutriments = models.ManyToManyField(Nutriment, through="Nutrition")
    category = models.CharField(max_length=300, default="unkonw")
    source = models.URLField(max_length=500, default="unkonw")
    image = models.URLField(max_length=500, default="unkonw")
    nutrition_grade = models.CharField(max_length=1, default="?")
    name = models.CharField(max_length=200, default="unkonw", unique=True)
    def __str__(self):
        return self.name

    def add_nutriment(self, nutriments_data):
        """create relation between aliment and nutriment"""
        for key, value in nutriments_data.items():
            nutriment = Nutriment.objects.get(name=key)
            nutrition = Nutrition(aliment=self, nutriment=nutriment, value=value)
            nutrition.save()

class Nutrition(models.Model):
    """nutrition model"""
    aliment = models.ForeignKey(Aliment, on_delete=models.CASCADE)
    nutriment = models.ForeignKey(Nutriment, on_delete=models.CASCADE)
    value = models.CharField(max_length=50)
    def __str__(self):
        return self.value
