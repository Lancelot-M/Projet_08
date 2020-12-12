from django.db import models

# Create your models here.

class Nutriment(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Aliment(models.Model):
    nutriments = models.ManyToManyField(Nutriment, through="Nutrition")
    category = models.CharField(max_length=300, default="unkonw")
    source = models.URLField(max_length=500, default="unkonw")
    image = models.URLField(max_length=500, default="unkonw")
    nutrition_grade = models.CharField(max_length=1, default="?")
    name = models.CharField(max_length=200, default="unkonw")
    def __str__(self):
        return self.name

class Nutrition(models.Model):
    aliment = models.ForeignKey(Aliment, on_delete=models.CASCADE)
    nutriment = models.ForeignKey(Nutriment, on_delete=models.CASCADE)
    value = models.CharField(max_length=50)