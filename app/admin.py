from django.contrib import admin

from users.models import Alquiler
from .models import Casa
# Register your models here.
admin.site.register(Casa)

admin.site.register(Alquiler)