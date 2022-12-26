from .models import *

from rest_framework import serializers


class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = '__all__'


class YieldDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = YieldData
        fields = '__all__'
