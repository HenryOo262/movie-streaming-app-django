from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Genre)
admin.site.register(models.Country)
admin.site.register(models.Cast)
admin.site.register(models.Director)
admin.site.register(models.Production)