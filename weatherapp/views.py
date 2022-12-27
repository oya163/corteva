from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import Http404

from .models import WeatherData, YieldData, Analytics
from .serializers import WeatherDataSerializer, YieldDataSerializer, AnalyticsSerializer


class WeatherDataList(APIView):
    def get(self, request, format=None):
        weatherdata_list = WeatherData.objects.all()
        serializer = WeatherDataSerializer(weatherdata_list, many=True)
        return Response(serializer.data)


class WeatherDataDetail(APIView):
    def get_object(self, id):
        try:
            return WeatherData.objects.get(id=id)
        except WeatherData.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        weatherdata = self.get_object(id)
        serializer = WeatherDataSerializer(weatherdata)
        return Response(serializer.data)


class WeatherDataByYear(APIView):
    def get(self, request, year, format=None):
        weatherdata = WeatherData.objects.filter(date__year=year)
        serializer = WeatherDataSerializer(weatherdata, many=True)
        return Response(serializer.data)


class WeatherDataByStationID(APIView):
    def get(self, request, station_id, format=None):
        weatherdata = WeatherData.objects.filter(station_id__exact=station_id)
        serializer = WeatherDataSerializer(weatherdata, many=True)
        return Response(serializer.data)


class YieldDataList(APIView):
    def get(self, request, format=None):
        yielddata_list = YieldData.objects.all()
        serializer = YieldDataSerializer(yielddata_list, many=True)
        return Response(serializer.data)


class YieldDataDetail(APIView):
    def get_object(self, id):
        try:
            return YieldData.objects.get(id=id)
        except YieldData.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        yielddata = self.get_object(id)
        serializer = YieldDataSerializer(yielddata)
        return Response(serializer.data)


class YieldDataByYear(APIView):
    def get_object(self, year):
        try:
            return YieldData.objects.get(date__year=year)
        except YieldData.DoesNotExist:
            raise Http404

    def get(self, request, year, format=None):
        yielddata = self.get_object(year)
        serializer = YieldDataSerializer(yielddata)
        return Response(serializer.data)


class AnalyticsList(APIView):
    def get(self, request, format=None):
        year = request.GET.get('year')
        station_id = request.GET.get('station_id')
        if year and station_id:
            analytics_list = Analytics.objects.filter(
                date__year=year).filter(station_id__exact=station_id)
        elif station_id:
            analytics_list = Analytics.objects.filter(
                station_id__exact=station_id)
        elif year:
            analytics_list = Analytics.objects.filter(date__year=year)
        else:
            analytics_list = Analytics.objects.all()
        serializer = AnalyticsSerializer(analytics_list, many=True)
        return Response(serializer.data)


class AnalyticsByDateList(APIView):
    def get(self, request, year, format=None):
        analytics_list = Analytics.objects.filter(date__year=year)
        serializer = AnalyticsSerializer(analytics_list, many=True)
        return Response(serializer.data)


class AnalyticsByStationIDList(APIView):
    def get(self, request, station_id, format=None):
        analytics_list = Analytics.objects.filter(
            station_id__startswith=station_id)
        serializer = AnalyticsSerializer(analytics_list, many=True)
        return Response(serializer.data)


class AnalyticsByYearAndStationIDList(APIView):
    def get(self, request, year, station_id, format=None):
        analytics_list = Analytics.objects.filter(
            date__year=year).filter(station_id__exact=station_id)
        serializer = AnalyticsSerializer(analytics_list, many=True)
        return Response(serializer.data)
