# CloudCast 🌤️

A simple weather forecasting web application integrated with Azure Functions and OpenWeatherMap API, built using Django.

## Overview

CloudCast is designed to provide accurate, real-time weather forecasts for various locations. This project demonstrates the integration of Django, Azure Functions, and external APIs to deliver seamless and responsive weather data.

## Features

- **Real-time weather forecasts**
- **Detailed weather summaries**
- **Azure Functions integration** for optimized API calls
- **Location-based search functionality**

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Django
- **Cloud Integration:** Azure Functions
- **Weather API:** OpenWeatherMap API

## Prerequisites

Make sure you have the following installed on your machine:

- Python 3.8+
- pip (Python package manager)
- Git

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/leyyenahsophie/CloudCast.git
    cd CloudCast
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Environment Variables Setup

Create a `.env` file at the project's root directory and paste the following:

```env
OPENWEATHER_API_KEY=YOUR_OPENWEATHER_API_KEY_HERE
AZURE_FUNCTION_KEY=YOUR_AZURE_FUNCTION_KEY_HERE
```

> ⚠️ **Note:** These keys are not included in the repository for security reasons. If you're a reviewer or professor and need access, please contact the author directly for the valid keys.

## Running the Project

After setting up the `.env` file and installing dependencies, run the following command to start the Django server:

```bash
python manage.py runserver
```

Access the application at:

```
http://localhost:8000/
```

## Directory Structure

```bash
CloudCast/
├── cloudcast/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── server/
│   ├── __init__.py
│   ├── function.json
│   └── requirements.txt
├── staticfiles/
├── weather/
│   ├── static/
│   │   └── style.css
│   ├── templates/
│   │   └── weather/
│   │       ├── daily_detail.html
│   │       ├── error.html
│   │       ├── forcast.html
│   │       └── home.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── .env
├── .gitignore
├── appsettings.json
├── db.sqlite3
├── manage.py
└── requirements.txt
```
