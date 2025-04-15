from django.urls import path
from . import views

app_name = 'alert'

urlpatterns = [
    path('', views.weather_view, name='get_weather'),  
    path('daily/<str:date>/', views.daily_detail_view, name='daily_detail_view'),
]
