from django.urls import path
from . import views

app_name = 'alert'

urlpatterns = [
    path('', views.weather_view, name='weather_view'),
    path('daily/<str:date>/', views.daily_detail_view, name='daily_detail_view'),
    path('get-weather/', views.get_weather_by_coords, name='get_weather_by_coords'),
]


