from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import Http404

from .models import WeatherData, YieldData
from .serializers import WeatherDataSerializer, YieldDataSerializer


class WeatherDataList(APIView):
    def get(self, request, format=None):
        weatherdata_list = WeatherData.objects.all()
        serializer = WeatherDataSerializer(weatherdata_list, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = WeatherDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

    # def put(self, request, id, format=None):
    #     weatherdata = self.get_object(id)
    #     serializer = WeatherDataSerializer(weatherdata, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, user_id, id, format=None):
    #     weatherdata = self.get_object(id)
    #     weatherdata.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class YieldDataList(APIView):
    def get(self, request, format=None):
        yielddata_list = YieldData.objects.all()
        serializer = YieldDataSerializer(yielddata_list, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = YieldDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
