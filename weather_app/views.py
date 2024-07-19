import urllib.request
import urllib.parse
import json
from django.shortcuts import render


def index(request):
    data = {}
    error_message = None

    if request.method == 'POST':
        city = request.POST['city']
        encoded_city = urllib.parse.quote(city)

        try:
            url = f'http://api.openweathermap.org/data/2.5/weather?q={encoded_city}&units=metric&appid=397f8b88403a047df3419ed463805a45&lang=ru'
            source = urllib.request.urlopen(url).read()
            list_of_data = json.loads(source)

            data = {
                "country_code": str(list_of_data['sys']['country']),
                "coordinate": str(list_of_data['coord']['lon']) + ', ' + str(list_of_data['coord']['lat']),
                "temp": str(list_of_data['main']['temp']) + ' °C',
                "pressure": str(list_of_data['main']['pressure']),
                "humidity": str(list_of_data['main']['humidity']),
                'main': str(list_of_data['weather'][0]['main']),
                'description': str(list_of_data['weather'][0]['description']),
                'icon': list_of_data['weather'][0]['icon'],
            }
        except urllib.error.HTTPError as e:
            if e.code == 404:
                error_message = "Город не найден. Пожалуйста, проверьте правильность ввода."
            else:
                error_message = "Произошла ошибка при получении данных о погоде. Пожалуйста, попробуйте еще раз позже."
        except Exception as e:
            error_message = f"Произошла неизвестная ошибка: {str(e)}"

    context = {
        'data': data,
        'error_message': error_message,
    }

    return render(request, 'index.html', context)

