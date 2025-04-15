from django.test import TestCase, Client
from django.urls import reverse
from .models import WeatherData
import json

# Create your tests here.

class WeatherAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create test data
        self.weather_data = WeatherData.objects.create(
            temperature=25.5,
            humidity=60,
            description="Sunny"
        )
        
    def test_weather_view_status_code(self):
        response = self.client.get(reverse('weather:home'))
        self.assertEqual(response.status_code, 200)
        
    def test_weather_data_model(self):
        self.assertEqual(self.weather_data.temperature, 25.5)
        self.assertEqual(self.weather_data.humidity, 60)
        self.assertEqual(self.weather_data.description, "Sunny")
        
    def test_daily_detail_view(self):
        # Set up session data
        session = self.client.session
        session['weather_data'] = [{
            'dt_txt': '2024-04-14 12:00:00',
            'main': {'temp': 25.5},
            'weather': [{'description': 'Sunny'}]
        }]
        session['city'] = 'Test City'
        session.save()
        
        response = self.client.get(reverse('weather:daily_detail_view', args=['2024-04-14']))
        self.assertEqual(response.status_code, 200)
