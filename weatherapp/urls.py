from django.urls import path, include

from weatherapp import views

urlpatterns = [
    path('weather/', views.WeatherDataList.as_view()),
    path('yield/', views.YieldDataList.as_view()),
]
