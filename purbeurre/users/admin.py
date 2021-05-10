"""Admin file"""

from django.contrib import admin
from users.models import MyUser, Rating, Myfood

admin.site.register(MyUser)
admin.site.register(Myfood)
admin.site.register(Rating)
