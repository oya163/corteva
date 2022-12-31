from datetime import datetime
from django.test import TestCase

from django.db import IntegrityError
from .models import WeatherData, YieldData, Analytics


class WeatherDataTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        WeatherData.objects.create(
            date=datetime.strptime('20221227', '%Y%m%d').date(),
            max_temp=19.99,
            min_temp=1.11,
            precipitation=15.55,
            station_id='USC00110072',
            created_at=datetime.now()
        )

        WeatherData.objects.create(
            date=datetime.strptime('20221227', '%Y%m%d').date(),
            max_temp=20.123,
            min_temp=0.123,
            precipitation=16.123,
            station_id='USC00110073',
            created_at=datetime.now()
        )

        WeatherData.objects.create(
            date=datetime.strptime('20221227', '%Y%m%d').date(),
            max_temp=10.123,
            min_temp=20.123,
            precipitation=16.123,
            station_id='USC00110074',
            created_at=datetime.now()
        )

    def test_weather_url(self):
        response = self.client.get('/api/weather/')
        self.assertEqual(response.status_code, 200)

    def test_weather_data(self):
        response = self.client.get('/api/weather/')
        self.assertEqual(len(response.json().get('results')), 3)
        self.assertEqual(response.json().get('results')[0]['id'], 1)
        self.assertEqual(response.json().get(
            'results')[0]['date'], '2022-12-27')
        self.assertEqual(response.json().get('results')[0]['max_temp'], 19.99)
        self.assertEqual(response.json().get('results')[0]['min_temp'], 1.11)
        self.assertEqual(response.json().get('results')
                         [0]['precipitation'], 15.55)
        self.assertEqual(response.json().get('results')[
                         0]['station_id'], 'USC00110072')

    def test_weather_station_url(self):
        response = self.client.get('/api/weather/?station_id=USC00110072')
        self.assertEqual(response.json().get('results')[
                         0]['station_id'], 'USC00110072')

    def test_weather_date_url(self):
        response = self.client.get('/api/weather/?date=2022-12-27')
        self.assertEqual(response.json().get(
            'results')[0]['date'], '2022-12-27')

    def test_weather_date_station_url(self):
        response = self.client.get(
            '/api/weather/?date=2022-12-27&station_id=USC00110072')
        self.assertEqual(response.json().get(
            'results')[0]['date'], '2022-12-27')
        self.assertEqual(response.json().get(
            'results')[0]['station_id'], 'USC00110072')


class YieldDataTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        YieldData.objects.create(
            date=datetime.strptime('20220101', '%Y%m%d').date(),
            corn_grain_yield=654321,
            created_at=datetime.now()
        )

        YieldData.objects.create(
            date=datetime.strptime('20210101', '%Y%m%d').date(),
            corn_grain_yield=123456,
            created_at=datetime.now()
        )

    def test_yield_url(self):
        response = self.client.get('/api/yield/')
        self.assertEqual(response.status_code, 200)

    def test_yield_date_query_params(self):
        response = self.client.get('/api/yield/?date=2022-01-01')
        self.assertEqual(response.json().get(
            'results')[0]['date'], '2022-01-01')


class AnalyticsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Analytics.objects.create(
            date=datetime.strptime('20220101', '%Y%m%d').date(),
            avg_max_temp=19.99,
            avg_min_temp=1.11,
            total_precipitation=15.55,
            station_id='USC00110072',
            created_at=datetime.now()
        )

        Analytics.objects.create(
            date=datetime.strptime('20210101', '%Y%m%d').date(),
            avg_max_temp=45.265,
            avg_min_temp=12.23,
            total_precipitation=78.23,
            station_id='USC00110073',
            created_at=datetime.now()
        )

    def test_analytics_url(self):
        response = self.client.get('/api/weather/stats/')
        self.assertEqual(response.status_code, 200)

    def test_analytics_id_query_params(self):
        response = self.client.get('/api/weather/stats/?id=1')
        self.assertEqual(response.json().get('results')[0]['id'], 1)

    def test_analytics_date_query_params(self):
        response = self.client.get('/api/weather/stats/?date=2022-01-01')
        self.assertEqual(response.json().get(
            'results')[0]['date'], '2022-01-01')

    def test_analytics_station_query_params(self):
        response = self.client.get(
            '/api/weather/stats/?station_id=USC00110072')
        self.assertEqual(response.json().get(
            'results')[0]['station_id'], 'USC00110072')

    def test_analytics_date_station_query_params(self):
        response = self.client.get(
            '/api/weather/stats/?date=2022-01-01&station_id=USC00110072')
        self.assertEqual(response.json().get(
            'results')[0]['date'], '2022-01-01')
        self.assertEqual(response.json().get(
            'results')[0]['station_id'], 'USC00110072')

    def test_integrity_error(self):
        with self.assertRaises(IntegrityError):
            Analytics.objects.create(
                date=datetime.strptime(
                    '20210101', '%Y%m%d').date(),
                avg_max_temp=3.265,
                avg_min_temp=22.23,
                total_precipitation=78.23,
                station_id='USC00110073',
                created_at=datetime.now()
            )
