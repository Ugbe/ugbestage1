from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.gis.geoip2 import GeoIP2
import requests

""" def hello(request):
    visitor_name = request.GET.get('visitor_name', 'Visitor')
    client_ip = get_client_ip(request)
    city, temperature = get_location_and_weather(client_ip)
    response_data = {
        "client_ip": client_ip,
        "location": city,
        "greeting": f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}"
    }
    return JsonResponse(response_data) """

def hello(request):
    visitor_name = request.GET.get('visitor_name', 'Visitor')
    client_ip, city = get_client_ip_and_city(request)
    temperature = get_weather(city)
    response_data = {
        "client_ip": client_ip,
        "location": city,
        "greeting": f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}"
    }
    return JsonResponse(response_data)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_location_and_weather(ip):
    # Initialize GeoIP2 object
    g = GeoIP2()

    try:
        city = g.city(ip)['city']
    except Exception:
        city = 'Unknown Location'
    
    # Use your actual OpenWeather API key
    weather_api_key = '80532158ef3c51b7377d75802928d76c'
    weather_api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
    
    try:
        weather_response = requests.get(weather_api_url).json()
        temperature = weather_response['main']['temp']
    except Exception:
        temperature = 'yet to be determined'

    return city, temperature
