import azure.functions as func
import json
import pytest
from manage import main  # Import the Azure function from manage.py

def test_weather_function_success(requests_mock):
    # Setup mock data
    city = "New York"
    mock_response = {
        "list": [
            {
                "main": {"temp": 72.5},
                "weather": [{"description": "Clear sky", "icon": "01d"}],
                "dt_txt": "2025-04-14 21:00:00"
            }
        ]
    }

    # This URL should match exactly how it's used in manage.py
    requests_mock.get(
        "https://cloudcast.azurewebsites.net/api/cloudcast",
        json=mock_response,
        status_code=200
    )

    # Simulate HTTP request
    req = func.HttpRequest(
        method='GET',
        url='/api/cloudcast',
        body=None,
        params={'city': city}
    )

    # Run Azure function
    result = main(req)

    # Assertions
    assert result.status_code == 200
    assert json.loads(result.get_body()) == mock_response
