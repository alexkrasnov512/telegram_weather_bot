from geopy import geocoders
import requests
from datetime import datetime


# Функция выводит координаты города
def cord_of_city(city: str):
    geolocator = geocoders.Nominatim(user_agent='telebot')
    latitude = geolocator.geocode(city).latitude
    longitude = geolocator.geocode(city).longitude
    return [latitude, longitude]


# Функция вывода общей погоды, из которой берется фактическая погода, погода на 7 часов и на 7 дней
def yandex_weather(latitude, longitude, token_yandex: str):
    url_yandex = f'https://api.weather.yandex.ru/v2/forecast?lat={latitude}&lon={longitude}&[lang=ru_RU]'
    yandex_resp = requests.get(url_yandex, headers={'X-Yandex-API-Key': token_yandex})
    conditions = {'clear': '☀', 'partly-cloudy': '🌤', 'cloudy': '⛅',
                  'overcast': '☁', 'drizzle': '🌧', 'light-rain': '🌧',
                  'rain': '🌧', 'moderate-rain': '🌧', 'heavy-rain': '🌧',
                  'continuous-heavy-rain': '🌧', 'showers': '🌧',
                  'wet-snow': '🌧', 'light-snow': '🌨', 'snow': '🌨',
                  'snow-showers': '🌨', 'hail': '🌨', 'thunderstorm': '🌩',
                  'thunderstorm-with-rain': '⛈', 'thunderstorm-with-hail': '⛈'
                  }
    wind_dir = {'nw': 'СЗ', 'n': 'С', 'ne': 'СВ', 'e': 'В', 'se': 'ЮВ', 's': 'Ю', 'sw': 'ЮЗ', 'w': 'З', 'c': 'Штиль'}
    yandex_json = yandex_resp.json()
    yandex_json['fact']['condition'] = conditions[yandex_json['fact']['condition']]
    yandex_json['fact']['wind_dir'] = wind_dir[yandex_json['fact']['wind_dir']]
    our_day = yandex_json['forecasts'][0]['hours']
    for i in our_day:
        i['condition'] = conditions[i['condition']]
        i['wind_dir'] = wind_dir[i['wind_dir']]
    next_day = yandex_json['forecasts'][1]['hours']
    for i in next_day:
        i['condition'] = conditions[i['condition']]
        i['wind_dir'] = wind_dir[i['wind_dir']]
    for i in yandex_json['forecasts']:
        for k, v in i['parts'].items():
            v['wind_dir'] = wind_dir[v['wind_dir']]
            v['condition'] = conditions[v['condition']]
    return yandex_json


# Функция выводит фактическую погоду
def fact_weather(weather):
    weatherfact = dict()
    params = {'temp': 'Температура', 'condition': 'Погодные условия', 'wind_dir': 'Направление ветра',
              'pressure_mm': 'Давление', 'wind_speed': 'Скорость ветра', 'humidity': 'Влажность'}
    for i in params:
        weatherfact[params[i]] = weather['fact'][i]
    return weatherfact


# Функция для создания словаря для каждого времени суток
def opredel(times_of_day):
    time_day_dict = dict()
    params = {'temp_min': 'Минимальная температура', 'temp_max': 'Максимальная температура',
              'temp_avg': 'Средняя температура', 'wind_dir': 'Направление ветра',
              'pressure_mm': 'Давление', 'wind_speed': 'Скорость ветра', 'humidity': 'Влажность',
              'condition': 'Погодные условия'}
    for i in params:
        time_day_dict[params[i]] = times_of_day[i]

    return time_day_dict


# Функция выводит погоду на 7 дней
def weather_on_7_days(weather):
    future = []
    times_of_day = {'morning': 'Утро', 'day': 'День', 'evening': 'Вечер', 'night': 'Ночь'}
    for i in weather['forecasts']:
        weather_for_days = dict()
        params_for_day = {'date': 'Число', 'sunrise': 'Время восхода солнца', 'sunset': 'Время заката солнца'}
        for y in params_for_day:
            weather_for_days[params_for_day[y]] = i[y]
        for z in times_of_day:
            weather_for_days[times_of_day[z]] = opredel(i['parts'][z])
        future.append(weather_for_days)
    return future


# Функция выводит погоду на 7 часов
def weather_on_7_hours(weather):
    weather_7_hours = list()
    time_hour = datetime.now().hour
    weather_on_hours = weather['forecasts'][0]['hours']
    weather_on_hours_next_day = weather['forecasts'][1]['hours']
    params_for_hours = {'hour': 'Время', 'temp': 'Температура', 'condition': 'Погодные условия',
                        'wind_dir': 'Направление ветра', 'pressure_mm': 'Давление',
                        'wind_speed': 'Скорость ветра', 'humidity': 'Влажность', 'icon': 'Иконка'}
    if time_hour+8 <= 24:
        for i in weather_on_hours[time_hour+1:time_hour+8]:
            mydict = dict()
            for y in params_for_hours:
                mydict[params_for_hours[y]] = i[y]
            weather_7_hours.append(mydict)
        return weather_7_hours
    else:
        counter = 0
        for i in weather_on_hours[time_hour+1:]:
            mydict = dict()
            for y in params_for_hours:
                mydict[params_for_hours[y]] = i[y]
            weather_7_hours.append(mydict)
            counter += 1
        for i in weather_on_hours_next_day[:7-counter]:
            mydict = dict()
            for y in params_for_hours:
                mydict[params_for_hours[y]] = i[y]
            weather_7_hours.append(mydict)
        return weather_7_hours
