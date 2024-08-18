from django.contrib import admin
from .models import Series, Season, SeriesResource, Episode

admin.site.register(Series)
admin.site.register(Season)
admin.site.register(Episode)
admin.site.register(SeriesResource)