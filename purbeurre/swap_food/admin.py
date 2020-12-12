from django.contrib import admin

from .models import Aliment, Nutrition, Nutriment

class AlimentAdmin(admin.ModelAdmin):
    pass

class NutrimentAdmin(admin.ModelAdmin):
    pass

class NutritionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Aliment, AlimentAdmin)
admin.site.register(Nutriment, NutrimentAdmin)
admin.site.register(Nutrition, NutritionAdmin)