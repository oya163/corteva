from django.urls import path

from weatherapp import views

urlpatterns = [
    path('weather/', views.WeatherDataList.as_view()),
    path('weather/id/<slug:id>/', views.WeatherDataDetail.as_view()),
    path('weather/year/<slug:year>/',
         views.WeatherDataByYear.as_view()),
    path('weather/stationid/<slug:station_id>/',
         views.WeatherDataByStationID.as_view()),
    path('yield/', views.YieldDataList.as_view()),
    path('yield/id/<slug:id>/', views.YieldDataDetail.as_view()),
    path('yield/year/<slug:year>/',
         views.YieldDataByYear.as_view()),
    path('weather/stats/', views.AnalyticsList.as_view()),
    path('weather/stats/year/<slug:year>/',
         views.AnalyticsByDateList.as_view()),
    path('weather/stats/stationid/<slug:station_id>/',
         views.AnalyticsByStationIDList.as_view()),
    path('weather/stats/yearandstationid/<slug:year>/<slug:station_id>/',
         views.AnalyticsByYearAndStationIDList.as_view()),
]
