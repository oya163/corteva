from rest_framework.generics import ListAPIView

from django_filters.rest_framework import DjangoFilterBackend

from .models import WeatherData, YieldData, Analytics
from .serializers import WeatherDataSerializer, YieldDataSerializer, AnalyticsSerializer


class WeatherDataList(ListAPIView):
    serializer_class = WeatherDataSerializer
    filter_backends = [DjangoFilterBackend]

    filterset_fields = ['id', 'date', 'station_id']

    def get_queryset(self):
        return WeatherData.objects.all()


class YieldDataList(ListAPIView):
    serializer_class = YieldDataSerializer
    filter_backends = [DjangoFilterBackend]

    filterset_fields = ['id', 'date']

    def get_queryset(self):
        return YieldData.objects.all()


class AnalyticsList(ListAPIView):
    serializer_class = AnalyticsSerializer
    filter_backends = [DjangoFilterBackend]

    filterset_fields = ['id', 'date', 'station_id']

    def get_queryset(self):
        return Analytics.objects.all()
