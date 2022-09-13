from telebot import *
from mycod import *
from prob import *


bot = TeleBot(TOKEN)
token_yandex = YandexTOKEN
lat = ''
long = ''
city = ''


@bot.message_handler(commands=['start'])
def welcome(message):
    sticker = open('static/AnimatedSticker.tgs', 'rb')
    bot.send_sticker(message.chat.id, sticker)
    bot.send_message(message.from_user.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, "
                                           "телеграмм-бот, созданный для сообщения "
                                           "погоды.".format(message.from_user, bot.get_me()), parse_mode='html')
    bot.send_message(message.from_user.id, "Вы можете написать город и получить погоду в нем")


@bot.message_handler(commands=['help'])
def command_help(message):
    bot.send_message(message.from_user.id, "Напишите любой город")


@bot.message_handler(content_types=['text'])
def weather_for_you(message):
    try:
        global lat, long, city
        city = message.text
        lat, long = cord_of_city(city)
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        item1 = types.KeyboardButton('Фактическая погода')
        item2 = types.KeyboardButton('Погода на 7 часов')
        item3 = types.KeyboardButton('Погода на 7 дней')
        markup.add(item1, item2, item3)
        bot.send_message(message.from_user.id, "Выберите погоду, которую хотите узнать", reply_markup=markup)
        bot.register_next_step_handler(message, weather_for_select)

    except AttributeError:
        bot.send_message(message.from_user.id, f'{message.from_user.first_name}! Я не нашел такой город!'
                                               f' Попробуй другой город')


def weather_for_select(message):
    yandex_w = yandex_weather(lat, long, YandexTOKEN)
    markup2 = types.ReplyKeyboardRemove()
    if message.text.lower() == "фактическая погода":
        yandex_fact_weather = fact_weather(yandex_w)
        bot.send_message(message.from_user.id, 'Погода в данный момент:''\n'
                                               f'{city}''\n'
                                               f'Температура: {yandex_fact_weather["Температура"]}\xb0С''\n'
                                               f'Погодные условия: {yandex_fact_weather["Погодные условия"]}''\n'
                                               f'Направление ветра: {yandex_fact_weather["Направление ветра"]}''\n'
                                               f'Давление: {yandex_fact_weather["Давление"]} мм.рт.ст.''\n'
                                               f'Скорость ветра: {yandex_fact_weather["Скорость ветра"]} м/с''\n'
                                               f'Влажность: {yandex_fact_weather["Влажность"]} %', reply_markup=markup2)
    elif message.text.lower() == "погода на 7 часов":
        yandex_7_hours_weather = weather_on_7_hours(yandex_w)
        bot.send_message(message.from_user.id, f'Погода на следующие 7 часов: \n')
        for i in yandex_7_hours_weather:
            bot.send_message(message.from_user.id, f'{i["Время"]}:00 \n'
                                                   f'{i["Температура"]}\xb0С, '
                                                   f'{i["Погодные условия"]}, '
                                                   f'{i["Направление ветра"]}, {i["Давление"]} мм.рт.ст., '
                                                   f'{i["Скорость ветра"]} м/с, {i["Влажность"]} %',
                                                   reply_markup=markup2)
    elif message.text.lower() == 'погода на 7 дней':
        yandex_7_days_weather = weather_on_7_days(yandex_w)
        bot.send_message(message.from_user.id, f'Погода на следующие 7 дней: \n')
        for i in yandex_7_days_weather:
            bot.send_message(message.from_user.id, f'{i["Число"][8:10]}.{i["Число"][5:7]}.{i["Число"][0:4]}\n'
                                                   f'Утро: '
                                                   f'{i["Утро"]["Средняя температура"]}\xb0С, '
                                                   f'{i["Утро"]["Погодные условия"]}, '
                                                   f'{i["Утро"]["Направление ветра"]}, '
                                                   f'{i["Утро"]["Давление"]} мм.рт.ст., '
                                                   f'{i["Утро"]["Скорость ветра"]} м/с, '
                                                   f'{i["Утро"]["Влажность"]} % \n'
                                                   f'День: '
                                                   f'{i["День"]["Средняя температура"]}\xb0С, '
                                                   f'{i["День"]["Погодные условия"]}, '
                                                   f'{i["День"]["Направление ветра"]}, '
                                                   f'{i["День"]["Давление"]} мм.рт.ст., '
                                                   f'{i["День"]["Скорость ветра"]} м/с, '
                                                   f' {i["День"]["Влажность"]} % \n'
                                                   f'Вечер: '                                                   
                                                   f'{i["Вечер"]["Средняя температура"]}\xb0С, '
                                                   f'{i["Вечер"]["Погодные условия"]}, '
                                                   f'{i["Вечер"]["Направление ветра"]}, '
                                                   f'{i["Вечер"]["Давление"]} мм.рт.ст., '
                                                   f'{i["Вечер"]["Скорость ветра"]} м/с, '
                                                   f'{i["Вечер"]["Влажность"]} % \n'
                                                   f'Ночь: '                                                   
                                                   f'{i["Ночь"]["Средняя температура"]}\xb0С, '
                                                   f'{i["Ночь"]["Погодные условия"]}, '
                                                   f'{i["Ночь"]["Направление ветра"]}, '
                                                   f'{i["Ночь"]["Давление"]} мм.рт.ст., '
                                                   f'{i["Ночь"]["Скорость ветра"]} м/с, '
                                                   f'{i["Ночь"]["Влажность"]} % \n', reply_markup=markup2)


bot.polling(none_stop=True, interval=0)
