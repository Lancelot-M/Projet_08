"""Admin file"""

from django.contrib import admin
from swap_food.models import Aliment, Nutrition, Nutriment

class AlimentAdmin(admin.ModelAdmin):
    """AlimentAdmin model"""

class NutrimentAdmin(admin.ModelAdmin):
    """NutrimentAdmin model"""

class NutritionAdmin(admin.ModelAdmin):
    """NutritionAdmin model"""

admin.site.register(Aliment, AlimentAdmin)
admin.site.register(Nutriment, NutrimentAdmin)
admin.site.register(Nutrition, NutritionAdmin)
