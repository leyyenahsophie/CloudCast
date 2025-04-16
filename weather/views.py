from django.shortcuts import render
from datetime import datetime, date
import requests
from collections import defaultdict

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
                original_data = weather_data  # Keep the original data for detailed plotting

                # Get today's date
                today_str = date.today().isoformat()

                # Filter out weather data for today
                current_weather = [entry for entry in weather_data if entry['dt_txt'].startswith(today_str)]

                # Get the first weather data entry for today
                if current_weather:
                    current_weather = current_weather[0]  # Take the first object

                for entry in weather_data:
                    date_obj = datetime.strptime(entry['dt_txt'], '%Y-%m-%d %H:%M:%S')
                    formatted_date = date_obj.strftime('%A, %b %d, %Y')
                    entry['formatted_date'] = formatted_date

                    # Daily summary calculations
                    date_str = date_obj.strftime('%Y-%m-%d')
                    temp = entry['main']['temp']
                    icon = entry['weather'][0]['icon']  # Extract the icon code

                    daily_summary[date_str]['temp_min'] = min(daily_summary[date_str]['temp_min'], temp)
                    daily_summary[date_str]['temp_max'] = max(daily_summary[date_str]['temp_max'], temp)
                    daily_summary[date_str]['icons'].append(icon)  # Add icon to list

                    if 'date' not in daily_summary[date_str]:
                        daily_summary[date_str]['date'] = date_obj.strftime('%A, %b %d, %Y')

                # Select the most common icon for each day
                for date_str, summary in daily_summary.items():
                    summary['icon'] = max(set(summary['icons']), key=summary['icons'].count)

            except requests.RequestException as e:
                print(f"An error occurred: {e}")

    # Prepare data for Chart.js
    labels = [entry['formatted_date'] for entry in original_data]
    temp_data = [entry['main']['temp'] for entry in original_data]
    daily_labels = [summary['date'] for summary in daily_summary.values()]
    temp_min_data = [summary['temp_min'] for summary in daily_summary.values()]
    temp_max_data = [summary['temp_max'] for summary in daily_summary.values()]

    return render(request, 'weather/forcast.html', {
        'current_weather': current_weather,
        'weather_data': weather_data,
        'daily_summary': sorted(daily_summary.items()),  # Convert dictionary to sorted list for template rendering
        'original_data': original_data,
        'city': city,
        'labels': labels,
        'temp_data': temp_data,
        'daily_labels': daily_labels,
        'temp_min_data': temp_min_data,
        'temp_max_data': temp_max_data,
    })


def daily_detail_view(request, date):
    # Retrieve weather data from session
    weather_data = request.session.get('weather_data')
    city = request.session.get('city')
    
    if not weather_data:
        # Handle the case where there's no weather data in session
        return render(request, 'weather/error.html', {'message': 'Detailed hourly temperature coming soon'})

    # Filter hourly data for the specified date
    hourly_data = [entry for entry in weather_data if entry['dt_txt'].startswith(date)]

    context = {
        'date': date,
        'hourly_data': hourly_data,
        'city': city,
    }

    return render(request, 'weather/daily_detail.html', context)
