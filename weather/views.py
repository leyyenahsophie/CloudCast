from django.shortcuts import render
from datetime import datetime, date
import requests
from collections import defaultdict
from django.http import JsonResponse
import os
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_GET

def weather_view(request):
    weather_data = None
    city = None
    daily_summary = defaultdict(lambda: {'temp_min': float('inf'), 'temp_max': float('-inf'), 'icons': []})
    original_data = []
    current_weather = None  # Variable to store the first weather data object

    if request.method == "POST":
        city = request.POST.get('city')

        if city:
            azure_function_url = "https://cloudcast.azurewebsites.net/api/cloudcast?code=AQoRLjvHeITqdyQ51yEl9h-gbvqrBrFZyvVZM_gJqLgrAzFuNfS-Fg%3D%3D"

            try:
                response = requests.get(azure_function_url, params={'city': city, 'units': 'imperial'})
                response.raise_for_status()
                weather_data = response.json()['list']
                original_data = weather_data

                today_str = date.today().isoformat()
                current_weather = [entry for entry in weather_data if entry['dt_txt'].startswith(today_str)]
                if current_weather:
                    current_weather = current_weather[0]

                for entry in weather_data:
                    date_obj = datetime.strptime(entry['dt_txt'], '%Y-%m-%d %H:%M:%S')
                    formatted_date = date_obj.strftime('%A, %b %d, %Y')
                    entry['formatted_date'] = formatted_date

                    date_str = date_obj.strftime('%Y-%m-%d')
                    temp = entry['main']['temp']
                    icon = entry['weather'][0]['icon']

                    daily_summary[date_str]['temp_min'] = min(daily_summary[date_str]['temp_min'], temp)
                    daily_summary[date_str]['temp_max'] = max(daily_summary[date_str]['temp_max'], temp)
                    daily_summary[date_str]['icons'].append(icon)

                    if 'date' not in daily_summary[date_str]:
                        daily_summary[date_str]['date'] = date_obj.strftime('%A, %b %d, %Y')

                for date_str, summary in daily_summary.items():
                    summary['icon'] = max(set(summary['icons']), key=summary['icons'].count)

            except requests.RequestException as e:
                print(f"An error occurred: {e}")

    labels = [entry['formatted_date'] for entry in original_data]
    temp_data = [entry['main']['temp'] for entry in original_data]
    daily_labels = [summary['date'] for summary in daily_summary.values()]
    temp_min_data = [summary['temp_min'] for summary in daily_summary.values()]
    temp_max_data = [summary['temp_max'] for summary in daily_summary.values()]

    return render(request, 'weather/forcast.html', {
        'current_weather': current_weather,
        'weather_data': weather_data,
        'daily_summary': sorted(daily_summary.items()),
        'original_data': original_data,
        'city': city,
        'labels': labels,
        'temp_data': temp_data,
        'daily_labels': daily_labels,
        'temp_min_data': temp_min_data,
        'temp_max_data': temp_max_data,
    })


def daily_detail_view(request, date):
    weather_data = request.session.get('weather_data')
    city = request.session.get('city')

    if not weather_data:
        return render(request, 'weather/error.html', {'message': 'Detailed hourly temperature coming soon'})

    hourly_data = [entry for entry in weather_data if entry['dt_txt'].startswith(date)]

    context = {
        'date': date,
        'hourly_data': hourly_data,
        'city': city,
    }

    return render(request, 'weather/daily_detail.html', context)


# Optional: a placeholder if you're still working on map integration
def get_weather_by_coords(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    if not lat or not lon:
        return JsonResponse({'error': 'Missing coordinates'}, status=400)

    # Get OpenWeatherMap API key from env
    OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY")
    if not OPENWEATHER_API_KEY:
        return JsonResponse({'error': 'Missing OpenWeatherMap API key in environment'}, status=500)

    try:
        # Step 1: Reverse geocode to get city name
        geo_url = (
            f"http://api.openweathermap.org/geo/1.0/reverse"
            f"?lat={lat}&lon={lon}&limit=1&appid={OWM_API_KEY}"
        )
        geo_resp = requests.get(geo_url)
        geo_resp.raise_for_status()
        geo_data = geo_resp.json()

        if not geo_data or 'name' not in geo_data[0]:
            return JsonResponse({'error': 'City not found for coordinates'}, status=400)

        city = geo_data[0]['name']
        country = geo_data[0].get('country', '')
        city_query = f"{city},{country}" if country else city

        # Step 2: Call your Azure cloudcast API using the city name
        azure_url = "https://cloudcast.azurewebsites.net/api/cloudcast"
        azure_response = requests.get(azure_url, params={
            'city': city_query,
            'units': 'imperial'
        })
        azure_response.raise_for_status()
        weather_data = azure_response.json()

        # Grab first result from Azure data
        current = weather_data['list'][0]
        return JsonResponse({
            'city': city,
            'temp': current['main']['temp'],
            'description': current['weather'][0]['description']
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)