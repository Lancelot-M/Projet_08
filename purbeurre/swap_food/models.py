from django.db import models

# Create your models here.

class Additive(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Aliment(models.Model):
    additives = models.ManyToManyField(Additive)
    allergens = models.CharField(max_length=500, default="unkonw")
    category = models.CharField(max_length=300, default="unkonw")
    image_s = models.URLField(max_length=500, default="unkonw")
    image = models.URLField(max_length=500, default="unkonw")
    ingredients = models.TextField(default="unkonw")
    #nutriments = models.ManyToManyField(Nutriment, on_delete=models.CASCADE)
    grade_food = models.CharField(max_length=1, default="U")
    name = models.CharField(max_length=200, default="unkonw")
    store = models.CharField(max_length=100, default="unkonw")
    def __str__(self):
        return self.name