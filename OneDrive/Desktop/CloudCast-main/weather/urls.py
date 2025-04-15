from django.urls import path
from . import views

app_name = 'weather'

urlpatterns = [
    path('', views.weather_view, name='home'),
    path('api/', views.weather_api_view, name='weather_api'),
    path('daily/<str:date>/', views.daily_detail_view, name='daily_detail_view'),
]