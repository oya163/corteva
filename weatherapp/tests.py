from datetime import datetime
from django.test import TestCase

from .models import WeatherData


class WeatherDataTestCase(TestCase):
    def setUp(self):
        WeatherData.objects.create(
            date=datetime.strptime('20221227', '%Y%m%d').date(),
            max_temp=19.99,
            min_temp=1.11,
            precipitation=15.55,
            station_id='USC00110072',
            created_at=datetime.now()
        )

        WeatherData.objects.create(
            date=datetime.strptime('20221226', '%Y%m%d').date(),
            max_temp=20.123,
            min_temp=0.123,
            precipitation=16.123,
            station_id='USC00110073',
            created_at=datetime.now()
        )

    def test_weather_data_ingestion(self):
        """WeatherData are ingested in test database correctly"""
        pass
