from rest_framework import serializers

from .models import WeatherData, YieldData, Analytics


class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = '__all__'


class YieldDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = YieldData
        fields = '__all__'


class AnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analytics
        fields = '__all__'
