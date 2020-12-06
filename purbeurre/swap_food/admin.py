from django.contrib import admin

from .models import Aliment, Additive

class AlimentAdmin(admin.ModelAdmin):
    pass

class AdditiveAdmin(admin.ModelAdmin):
    pass

admin.site.register(Aliment, AlimentAdmin)
admin.site.register(Additive, AdditiveAdmin)