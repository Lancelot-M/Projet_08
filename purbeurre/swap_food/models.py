from django.db import models

# Create your models here.
class Aliments(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    note = models.CharField(max_length=1)
    photo = models.URLField(max_length=500)
    def __str__(self):
        return self.name