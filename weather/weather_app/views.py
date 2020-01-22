import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=af311794fa76ee721b22d108f386610a'

    error_message = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()

                if r['cod'] == 200:
                    form.save()
                else:
                    error_message = "City doesn't exist in the world!"
            else:
                error_message = 'City already exists in the database!'

        if error_message:
            message = error_message
            message_class = 'is-danger'
        else:
            message = 'City added successfully!'
            message_class = 'is-success'

    form = CityForm()
    cities = City.objects.all()
    weather_data = []

    for city in cities:
        r = requests.get(url.format(city)).json()
        city_weather = {
                    'city': city.name,
                    'temperature': r['main']['temp'],
                    'description': r['weather'][0]['description'],
                    'icon': r['weather'][0]['icon'],
                    'wind_speed': r['wind']['speed'],
                    'pressure': r['main']['pressure'],
                    'feels_like': r['main']['feels_like'],
                    'temp_min': r['main']['temp_min'],
                    'temp_max': r['main']['temp_max'],
                    'humidity': r['main']['humidity'],
                }
        weather_data.append(city_weather)

    context = {
        'weather_data': weather_data,
        'form': form,
        'message': message,
        'message_class': message_class,
    }

    return render(request, 'weather_app/index.html', context)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')



