"""Admin file"""

from django.contrib import admin
from users.models import MyUser, Rating

admin.site.register(MyUser)
admin.site.register(Rating)
