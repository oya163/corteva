from django.urls import path

from weatherapp import views

urlpatterns = [
    path('weather/', views.WeatherDataList.as_view()),
    path('yield/', views.YieldDataList.as_view()),
    path('weather/stats/', views.AnalyticsList.as_view()),
]
