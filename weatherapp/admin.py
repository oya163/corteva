from django.contrib import admin

from .models import WeatherData, YieldData, Analytics

admin.site.register(WeatherData)
admin.site.register(YieldData)
admin.site.register(Analytics)
