from django.db import models

# Create your models here.

class WeatherData(models.Model):
    temperature = models.FloatField()
    humidity = models.IntegerField()
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.description} - {self.temperature}°C"
