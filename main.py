

import colorama
import pyttsx3
import os
import random
import webbrowser
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
from pyowm import OWM
from pyowm.utils.config import get_default_config
import datetime
import requests
from bs4 import BeautifulSoup
import sys
import wikipedia as wiki
import configparser
import re
import COVID19Py
class Assistant:
settings = configparser.ConfigParser() # синтаксический анализатор файлов конфигурации
settings.read('settings.ini') # считывание файла с настройками
config_dict = get_default_config() # Инициализация get_default_config()
config_dict['language'] = 'ru' # Установка языка
ndel = ['не мог бы ты', 'пожалуйста', 'текущее', 'сейчас'] # список слов на удаление из запроса
commands = ['Привет', 'добрый вечер', 'доброе утро', 'добрый день', # список команд
'выключи ноутбук', 'выключи компьютер',
'пока', 'отключись',
'покажи список команд',
'подбрось монетку', 'подкинь монетку', 'кинь монетку',
'найди', 'найти', 'ищи', 'кто такой',
'как дела', 'как жизнь', 'как настроение', 'как ты',
'текущее время', 'сколько времени', 'сколько время', 'сейчас времени',
'который час',
'какая погода', 'погода', 'погода на улице', 'какая погода на улице',
'спасибо',
'ты здесь', 'не спишь',
'просыпайся', 'я вернулся', 'просыпайся я вернулся', 'я вернулась',
'просыпайся я вернулась',
'включи балаболку', 'балаболка',
'отбой', 'вздремни пока', 'режим ожидания', 'включи режим ожидания',
'открой калькулятор', 'включи калькулятор',
'какой сегодня день', 'какой сегодня месяц', 'какое сегодня число',
'включи браузер', 'открой браузер'
'открой настройки конфигуратора', 'настройки конфигуратора',
'расскажи анекдот', 'анекдот', 'рассмеши меня',
'напомни', 'напоминалка',
'статистика заболеваемости', 'статистика коронавируса',
'заболеваемость коронавирусом', 'какая статистика заболеваемости', ]
def __init__(self):
self.r = sr.Recognizer() # получает голос, чтобы передать на сервера гугл
self.engine = pyttsx3.init()
self.text = ''
27
self.j = 0
self.fr = 0
self.covid19 = COVID19Py.COVID19()
self.task_number = 0
wiki.set_lang('ru')
self.cmds = {
'привет': self.hello(),
'выруби компьютер': self.shut, 'выключи комп': self.shut, 'выключи компьютер':
self.shut,
'выключай компьютер': self.shut,
'подбрось монетку': self.monetka, 'подкинь монетку': self.monetka, 'кинь монетку':
self.monetka,
'найди': self.web_search, 'найти': self.web_search, 'ищи': self.web_search, 'кто такой':
self.web_search,
'что такое': self.web_search,
'как дела': self.howyou, 'как жизнь': self.howyou, 'как настроение': self.howyou, 'как
ты': self.howyou,
'пока': self.quite, 'вырубись': self.quite, 'отключись': self.quite,
'покажи список команд': self.show_cmds,
'открой браузер': self.brows, 'открой интернет': self.brows, 'включи браузер':
self.brows,
'текущее время': self.timethis, 'сейчас времени': self.timethis, 'который час':
self.timethis,
'сколько времени': self.timethis, 'сколько время': self.timethis,
'какая погода': self.weather_pogoda, 'погода': self.weather_pogoda, 'погода на
улице': self.weather_pogoda,
'какая погода на улице': self.weather_pogoda,
'спасибо': self.senks,
'ты здесь': self.youarehere, 'не спишь': self.youarehere,
'включи балаболку': self.balabolka, 'балаболка': self.balabolka,
'вздремни пока': self.pause, 'режим ожидания': self.pause,
'включи режим ожидания': self.pause,
'открой калькулятор': self.calc, 'включи калькулятор': self.calc,
'какой сегодня день': self.days, 'какой сегодня месяц': self.days, 'какое сегодня
число': self.days,
'открой настройки конфигуратора': self.perezapis, 'настройки конфигуратора':
self.perezapis,
'расскажи анекдот': self.anekdot, 'анекдот': self.anekdot, 'рассмеши меня':
self.anekdot,
'напомни': self.reminder, 'напоминалка': self.reminder,
'статистика заболеваемости': self.covid_stat, 'статистика коронавируса':
self.covid_stat,
'заболеваемость коронавирусом': self.covid_stat, 'какая статистика
заболеваемости': self.covid_stat,
}
def show_cmds(self): # выводит на экран список доступных команд
self.is_not_used()
for i in Assistant.commands:
print(i)
time.sleep(1)
def anekdot(self): # рассказывает анекдот
s = requests.get('http://anekdotme.ru/random')
b = BeautifulSoup(s.text, "html.parser")
p = b.select('.anekdot_text')
s = (p[0].getText().strip())
reg = re.compile('[^a-zA-Zа-яА-я ^0-1-2-3-4-5-6-7-8-9.,!?-]')
s = reg.sub('', s)
28
self.talk(s)
def covid_stat(self): # показывает статистику по коронавирусу
location = self.covid19.getLocationByCountryCode("RU")
date = location[0]['last_updated'].split("T")
ctime = date[1].split(".")
changes = self.covid19.getLatestChanges()
final_message = f"Данные по стране: Россия\n" \
f"Последнее обновление: {date[0]} {ctime[0]}\nПоследние
данные:\n" \
f"Заболевших: {location[0]['latest']['confirmed']:,}\nСмертей: " \
f"{location[0]['latest']['deaths']:,}"
self.talk(final_message)
def web_search(self): # веб поиск
tr = 0
k = ['Вот что я нашла по вашему запросу', 'Вот что мне удалось найти', 'Вот что я
нашла']
variants = ['найди', 'что такое', 'кто такой', 'найти', 'ищи']
for i in variants:
if (i in self.text) & (tr == 0):
repl = self.text
repl = repl.replace(i, '').strip()
self.talk(random.choice(k))
webbrowser.open(f'https://www.google.com/search?q={repl}&oq={repl}'
f'81&aqs=chrome..69i57j46i131i433j0l5.2567j0j7&sourceid=chrome&ie=UTF-8')
try:
info = wiki.summary(repl)
self.talk(((info[0:230]).replace('англ', '')).replace('род.',
'родился').replace('(.', '')
.replace(')', '').replace(';', ''))
except wiki.exceptions.PageError:
pass
except wiki.exceptions.WikipediaException:
pass
del repl
tr = 0
self.text = ''
def balabolka(self): # озвучка текста
num = 1
while num == 1:
k = input("Введите текст который надо озвучить: ")
self.talk(k)
num = num + 1
def monetka(self): # "подбрасывает" монетку
self.talk("Подбрасываю...")
k = ["Выпал Орёл", "Выпала Решка"]
self.talk(random.choice(k))
def youarehere(self): # чуть чуть говорит
k = ['Слушаю вас', 'К вашим услугам']
self.talk(random.choice(k))
def senks(self): # чуть чуть говорит
k = ['Обращайтесь', 'Всегда рада помочь', 'Не за что!']
self.talk(random.choice(k))
29
def clear_task(self): # удаляет ключевые слова из запроса
for z in Assistant.ndel:
self.text = self.text.replace(z, '').strip()
self.text = self.text.replace(' ', ' ').strip()
def hello(self): # здоровается при запуске
now = datetime.datetime.now()
if int(now.hour) >= 6 and now.hour < 12:
z = ["Доброе утро, чем могу быть полезна?", 'Что вам угодно?', 'Привет. Чем-нибудь
помочь?']
self.talk(random.choice(z))
elif int(now.hour) >= 12 and now.hour < 18:
z = ["Добрый день, чем могу быть полезна?", 'Что вам угодно?', 'Привет. Чем-
нибудь помочь?']
self.talk(random.choice(z))
elif int(now.hour) >= 18 and now.hour < 23:
z = ["Добрый вечер, чем могу быть полезна?", 'Что вам угодно?', 'Привет. Чем-
нибудь помочь?']
self.talk(random.choice(z))
else:
z = ["Доброй ночи, чем могу быть полезна?", 'Что вам угодно?', 'Привет. Чем-нибудь
помочь?']
self.talk(random.choice(z))
def quite(self): # функция выхода из программы
x = ['Надеюсь мы скоро увидимся!', 'Рада была помочь', 'Я отключаюсь']
self.talk(random.choice(x))
self.engine.stop()
os.system('cls')
sys.exit(0)
def is_not_used(self):
pass
def cfile(self):
self.is_not_used()
if self.fr == 0:
file = open('settings.ini', 'w', encoding='UTF-8')
file.write('[SETTINGS]\ncountry = RU\nplace = Kazan\nbrowser = yandex\nfcreated =
1')
file.close()
self.fr += 1
def perezapis(self): # перезапись данных в файл
self.is_not_used()
onoff = 1
self.talk("Введите номер переменной которую вы хотите изменить")
while onoff == 1:
numb = input(("Изменить город '1'\nИзменить страну '2'\nИзменить браузер '3'"
"\nВыключить режим редактирования данных '0'"
"\nВведите номер переменной в которой хотите изменить значение: "))
if str(numb) == "1":
with open('settings.ini', 'r') as f:
old = f.read()
nplace = Assistant.settings['SETTINGS']['place']
cnew = input("Введите город (Пример Kazan): ")
new = old.replace(nplace, cnew)
with open('settings.ini', 'w') as f:
f.write(new)
30
print("Город успешно изменён!")
elif str(numb) == "2":
with open('settings.ini', 'r') as f:
old = f.read()
ncountry = Assistant.settings['SETTINGS']['country']
cnew = input("Введите код страны (Пример RU): ")
new = old.replace(ncountry, cnew)
with open('settings.ini', 'w') as f:
f.write(new)
print("Страна успешно изменена")
elif str(numb) == "3":
with open('settings.ini', 'r') as f:
old = f.read()
nbrows = Assistant.settings['SETTINGS']['browser']
cnew = input("Введите название браузера (Например chrome, yandex, opera):
")
new = old.replace(nbrows, cnew)
with open('settings.ini', 'w') as f:
f.write(new)
print("Браузер успешно изменён")
elif str(numb) == "0":
print("Режим редактирования выключен")
onoff = onoff + 1
def weather_pogoda(self): # говорит погоду
place = Assistant.settings['SETTINGS']['place']
country = Assistant.settings['SETTINGS']['country'] # Переменная для записи страны/кода
страны
country_and_place = place + ", " + country # Запись города и страны в одну переменную
через запятую
owm = OWM('ВАШ КЛЮЧ С САЙТА https://openweathermap.org/api')
mgr = owm.weather_manager() # Инициализация owm.weather_manager()
observation = mgr.weather_at_place(country_and_place)
w = observation.weather
status = w.detailed_status # Узнаём статус погоды в городе и записываем в
переменную status
w.wind() # Узнаем скорость ветра
humidity = w.humidity # Узнаём Влажность и записываем её в переменную humidity
temp = w.temperature('celsius')['temp'] # Узнаём температуру в градусах по цельсию
self.talk("В городе " + str(place) + " сейчас " + str(status))
self.talk("Температура " + str(round(temp)) + " градусов по цельсию")
self.talk("Влажность составляет " + str(humidity) + "%")
self.talk("Скорость ветра " + str(w.wind()['speed']) + " метров в секунду")
if int(temp) <= -19 + 4:
self.talk("Сегодня очень холодно, надевайте термобельё и постарайтесь
поменьше "
находиться на улице, не забудьте про тёплые перчатки и шарф")
elif int(temp) <= -15 + 4:
self.talk("Сегодня на улице достаточно холодно, одевайтесь теплее и не забудьте
взять перчатки")
elif int(temp) <= -10 + 4:
self.talk("Сегодня холодно, надевайте зимнюю куртку и шапку, также не забудьте
взять с собой перчатки")
elif int(temp) <= -5 + 4:
self.talk("Сегодня относительно прохладно, надевайте теплую куртку и пальто")
elif int(temp) <= 0 + 4:
self.talk("Сегодня прохладно, рекомендую надеть пальто")
elif int(temp) <= 5 + 4:
self.talk("Сегодня на улице прохладно надевайте куртку или плащ")
31
elif int(temp) <= 10 + 4:
self.talk("На улице прохладно, не рекомендую одеваться лёгко, надевайте штаны
и ветровку")
elif int(temp) <= 15 + 4:
self.talk("На улице достаточно тепло, но рекомендую надеть ветровку")
elif int(temp) <= 20 + 4:
self.talk("Сегодня очень тепло, надевайте шорты и футболку")
elif int(temp) <= 21 + 999:
self.talk("Сегодня жара, надевайте шорты и футболку")
else:
pass
if str(status) == "дождь":
self.talk("Не забудьте взять с собой зонтик")
def brows(self): # открывает браузер
webbrowser.open('https://google.com')
self.talk("Браузер открыт!")
def pause(self): # переход и выход в режим ожидания
num = 1
m = ['Переключаюсь в режим ожидания', 'Если буду нужна, обращайтесь']
self.talk(random.choice(m))
while num == 1:
self.engine.runAndWait()
self.text = self.listen()
if (fuzz.ratio(self.text, 'просыпайся') > 60) or (fuzz.ratio(self.text, "проснись") > 60
or
(fuzz.ratio(self.text, "просыпайся я вернулся") > 60)):
k = ['Что вам угодно?', 'Я вас слушаю', 'Чем могу быть полезна?', 'Чем вам помочь?',
'К вашим услугам']
self.talk(random.choice(k))
num = num + 1
def reminder(self): # напоминалка
remind = str(input("Напишите, что мне вам напомнить? "))
local_time = float(input("Через сколько минут? "))
local_time = local_time
time.sleep(local_time)
self.talk(remind)
print(remind)
def howyou(self): # чуть-чуть общается
k = ["Всегда готова к работе!", "Отлично!", "Вполне сносно"]
self.talk(random.choice(k))
def calc(self): # открывает калькулятор
self.talk('Открываю калькулятор')
os.system('calc')
def days(self): # говорит какой сегодня день
now = datetime.datetime.now()
month = ''
day = ''
if now.month == 1:
month = 'Января'
elif now.month == 2:
month = 'Февраля'
elif now.month == 3:
month = 'Марта'
32
elif now.month == 4:
month = 'Апреля'
elif now.month == 5:
month = 'Мая'
elif now.month == 6:
month = 'Июня'
elif now.month == 7:
month = 'Июля'
elif now.month == 8:
month = 'Августа'
elif now.month == 9:
month = 'Сентября'
elif now.month == 10:
month = 'Октября'
elif now.month == 11:
month = 'Ноября'
elif now.month == 12:
month = 'Декабря'
if now.day == 1:
day = 'Первое'
if now.day == 2:
day = 'Второе'
if now.day == 3:
day = 'Третье'
if now.day == 4:
day = 'Четвётое'
if now.day == 5:
day = 'Пятое'
if now.day == 6:
day = 'Шестое'
if now.day == 7:
day = 'Седьмое'
if now.day == 8:
day = 'Восьмое'
if now.day == 9:
day = 'Девятое'
if now.day == 10:
day = 'Десятое'
if now.day == 11:
day = 'Одиннадцатое'
if now.day == 12:
day = 'Двенадцатое'
if now.day == 13:
day = 'Тринадцатое'
if now.day == 14:
day = 'Четырнадцатое'
if now.day == 15:
day = 'Пятнадцатое'
if now.day == 16:
day = 'Шестнадцатое'
if now.day == 17:
day = 'Семнадцатое'
if now.day == 18:
day = 'Восемнадцатое'
if now.day == 19:
day = 'Девятнадцатое'
if now.day == 20:
day = 'Двадцатое'
if now.day == 21:
33
day = 'Двадцать первое'
if now.day == 22:
day = 'Двадцать второе'
if now.day == 23:
day = 'Двадцать третье'
if now.day == 24:
day = 'Двадцать четвёртое'
if now.day == 25:
day = 'Двадцать пятое'
if now.day == 26:
day = 'Двадцать шестое'
if now.day == 27:
day = 'Двадцать седьмое'
if now.day == 28:
day = 'Двадцать восьмое'
if now.day == 29:
day = 'Двадцать девятое'
if now.day == 30:
day = 'Тридцатое'
if now.day == 31:
day = 'Тридцать первое'
self.talk('Сегодня ' + str(day) + ' ' + str(month))
def timethis(self): # говорит время
now = datetime.datetime.now()
self.talk("Сейчас " + str(now.hour) + ":" + str(now.minute))
def shut(self): # выключает компьютер
self.talk("Подтвердите действие!")
self.text = self.listen()
print(self.text)
if (fuzz.ratio(self.text, 'подтвердить') > 60) or (fuzz.ratio(self.text, "подтверждаю") > 60):
self.talk('Действие подтверждено')
self.talk('До скорых встреч!')
os.system('shutdown /s /f /t 10')
self.quite()
elif fuzz.ratio(self.text, 'отмена') > 60:
self.talk("Действие не подтверждено")
else:
self.talk("Действие не подтверждено")
def listen(self):
self.text = ''
with sr.Microphone() as sourse: # возьми микрофон как источник
print(colorama.Fore.GREEN + "Я вас слушаю...")
self.r.adjust_for_ambient_noise(sourse) # слушаем аудио
audio = self.r.listen(sourse, phrase_time_limit=3)
try:
self.text = (self.r.recognize_google(audio, language="ru-RU")).lower() #
понижает регистр текста
except sr.UnknownValueError: # если не получилось распознать, что мы сказали
return 'Listening error'
except sr.RequestError as e: # если что-то пошло не так с соединением
return 'Connecting error'
os.system('cls')
self.clear_task()
return self.text
def comparison(self, x): # осуществляет поиск самой подходящей под запрос функции
34
commands = Assistant.commands
ans = ''
for i in range(len(commands)):
k = fuzz.ratio(x, commands[i])
if (k > 70) & (k > self.j):
ans = commands[i]
self.j = k
return str(ans)
def cmd_exe(self):
self.web_search()
self.text = self.comparison(self.text)
print(colorama.Fore.LIGHTCYAN_EX + self.text)
if self.text in self.cmds:
if (self.text != 'пока') & (self.text != 'покажи список команд') \
& (self.text != 'текущее время') & (self.text != 'сколько времени') \
& (self.text != 'сколько время') & (self.text != 'сейчас времени') & (self.text != 'который час')
\
& (self.text != 'какая погода') \
& (self.text != 'Привет') \
& (self.text != 'привет') & (self.text != 'доброе утро') & (self.text != 'добрый день') \
& (self.text != 'добрый вечер') \
& (self.text != 'как дела') & (self.text != 'как жизнь') & (self.text != 'как настроение') \
& (self.text != 'как ты') \
& (self.text != 'напомни') & (self.text != 'напоминалка') \
& (self.text != 'погода') & (self.text != 'погода на улице') \
& (self.text != 'какая погода на улице') \
& (self.text != 'выруби компьютер') & (self.text != 'выключи комп') \
& (self.text != 'выключи компьютер') \
& (self.text != 'выключи компьютер') & (self.text != 'выключай компьютер') \
& (self.text != 'спасибо') \
& (self.text != 'открой калькулятор') & (self.text != 'включи калькулятор') \
& (self.text != 'ты здесь') & (self.text != 'не спишь') \
& (self.text != 'какой сегодня день') & (self.text != 'какой сегодня месяц') \
& (self.text != 'какое сегодня число') \
& (self.text != 'открой браузер') & (self.text != 'открой интернет') & (
self.text != 'включи браузер') \
& (self.text != 'включи балаболку') & (self.text != 'балаболка') \
& (self.text != 'расскажи анекдот') & (self.text != 'анекдот') & (self.text != 'расмеши меня')\
& (self.text !='статистика заболеваемости')& (self.text !='статистика коронавируса')\
& (self.text !='заболеваемость коронавирусом'):
k = ['Секундочку', 'Сейчас сделаю', 'Уже выполняю']
self.talk(random.choice(k))
self.cmds[self.text]()
elif self.text == '':
pass
else:
print('Команда не найдена!')
self.task_number += 1
if self.task_number % 10 == 0:
self.talk('У вас будут еще задания?')
self.engine.runAndWait()
self.engine.stop()
def talk(self, text):
print(colorama.Fore.LIGHTGREEN_EX + text)
self.engine.say(text)
self.engine.runAndWait()
35
os.system('cls') # очистка экрана
def main(self):
fr = 0
try:
fcr = Assistant.settings['SETTINGS']['fcreated']
if int(fcr) != 1:
if fr == 0:
self.cfile()
fr += 1
except KeyError:
print("Файл settings.ini был создан!")
self.talk("Для настройки конфигурации скажите 'Открой настройки
конфигуратора' ")
fr += 1
self.cfile()
try:
self.listen()
if self.text != '':
self.cmd_exe()
self.j = 0
except UnboundLocalError:
pass
except NameError:
pass
except TypeError:
pass
except IndentationError:
pass
except IndexError:
pass
except ValueError:
pass
except KeyError:
pass
except NotImplementedError:
pass
except SyntaxError:
pass
except AttributeError:
pass
while True: # пока программа не закроется, выполняем следующие команды
Assistant().main()
5. Ассистент, созданный при помощи машинного обучения
import pyttsx3
import speech_recognition as sr
import json
import random
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn.model_selection import train_test_split
from PyQt5 import QtWidgets, QtCore
36
import newinterface_ui
import threading
with open('NEW_BIG_BOT_CONFIG.json', 'r') as f:
BOT_CONFIG = json.load(f)
work = True
class Assistant(QtWidgets.QMainWindow, newinterface_ui.Ui_MainWindow, threading.Thread):
def __init__(self):
super(Assistant, self).__init__()
self.setupUi(self) #отображение интерфейса
self.r = sr.Recognizer()
#####
self.pushButton.pressed.connect(self.start_thread_assist) # кнопка слушать
self.pushButton_2.pressed.connect(self.off) # кнопка стоп
#####
def cleaner(self, text):
cleaned_text = ''
for ch in text.lower():
if ch in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz ':
cleaned_text = cleaned_text + ch
return cleaned_text
def match(self, text, example):
return nltk.edit_distance(text, example) / len(example) < 0.4 if len(example) > 0 else False
def get_intent(self, text):
for intent in BOT_CONFIG['intents']:
if 'examples' in BOT_CONFIG['intents'][intent]:
for example in BOT_CONFIG['intents'][intent]['examples']:
if self.match(self.cleaner(text), self.cleaner(example)):
return intent
def ml_model(self, text):
X = []
y = []
for intent in BOT_CONFIG['intents']:
if 'examples' in BOT_CONFIG['intents'][intent]:
X += BOT_CONFIG['intents'][intent]['examples']
y += [intent for i in range(len(BOT_CONFIG['intents'][intent]['examples']))]
# Создаем обучающую выборку для ML-модели
vectorizer = CountVectorizer(preprocessor=self.cleaner, ngram_range=(1, 3), stop_words=['а', 'и'])
# Создаем векторайзер – объект для превращения текста в вектора
vectorizer.fit(X)
X_vect = vectorizer.transform(X)
# Обучаем векторайзер на нашей выборке
X_train_vect, X_test_vect, y_train, y_test = train_test_split(X_vect, y, test_size=0.3)
# Разбиваем выборку на train и на test
37
log_reg = LogisticRegression()
log_reg.fit(X_train_vect, y_train)
log_reg.score(X_test_vect, y_test)
sgd = SGDClassifier() # Создаем модель
sgd.fit(X_train_vect, y_train) # Обучаем модель
sgd.score(X_test_vect, y_test) # Проверяем качество модели на тестовой выборке
sgd.fit(X_vect, y)
sgd.score(X_vect, y) # Смотрим качество классификации
return sgd.predict(vectorizer.transform([text]))[0]
def intenter(self, text):
intent = self.get_intent(text)
if intent is None:
intent = self.ml_model(text)
self.talk(random.choice(BOT_CONFIG['intents'][intent]['responses']))
def talk(self, text):
self.engine = pyttsx3.init(debug=True)
print(text)
item = QtWidgets.QListWidgetItem()
item.setTextAlignment(QtCore.Qt.AlignLeft)
item.setText('MORGAN:' + '\n' + text)
self.listWidget.addItem(item)
self.engine.say(text)
self.engine.runAndWait()
def listen(self):
with sr.Microphone() as source:
print("Скажите что-нибудь...")
self.r.adjust_for_ambient_noise(source) # Этот метод нужен для автоматического
понижени уровня шума
audio = self.r.listen(source)
try:
text = self.r.recognize_google(audio, language="ru-RU").lower()
except sr.UnknownValueError:
pass
print(text)
item = QtWidgets.QListWidgetItem()
item.setTextAlignment(QtCore.Qt.AlignRight)
item.setText('Вы сказали:' + '\n' + text)
self.listWidget.addItem(item)
return text
def off(self):
global work
work = False
def main(self):
global work
while work:
try:
self.intenter(self.listen())
except:
pass
38
def start_thread_assist(self):
thread = threading.Thread(target=self.main, args=())
thread.start()
App = QtWidgets.QApplication([])
window = Assistant()
window.show()
App.exec()
6. Дизайн для ассистента с машинным обучением
from PyQt5 import QtCore, QtGui, QtWidgets
class Ui_MainWindow(object):
def setupUi(self, MainWindow):
MainWindow.setObjectName("MainWindow")
MainWindow.resize(441, 656)
font = QtGui.QFont()
font.setPointSize(8)
MainWindow.setFont(font)
MainWindow.setStyleSheet("background-color: #b0abab;")
self.centralwidget = QtWidgets.QWidget(MainWindow)
self.centralwidget.setObjectName("centralwidget")
self.pushButton = QtWidgets.QPushButton(self.centralwidget)
self.pushButton.setGeometry(QtCore.QRect(20, 570, 171, 61))
font = QtGui.QFont()
font.setPointSize(23)
self.pushButton.setFont(font)
self.pushButton.setStyleSheet("QPushButton {\n"
" background-color: #c7c3c3;\n"
" border-radius: 6;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
" background-color: #d9d4d4;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
" background-color: #8a8888;\n"
"}")
self.pushButton.setObjectName("pushButton")
self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
self.pushButton_2.setGeometry(QtCore.QRect(250, 570, 171, 61))
font = QtGui.QFont()
font.setPointSize(23)
self.pushButton_2.setFont(font)
self.pushButton_2.setStyleSheet("QPushButton {\n"
" background-color: #c7c3c3;\n"
" border-radius: 6;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
" background-color: #d9d4d4;\n"
"}\n"
39
"\n"
"QPushButton:pressed {\n"
" background-color: #8a8888;\n"
"}")
self.pushButton_2.setObjectName("pushButton_2")
self.listWidget = QtWidgets.QListWidget(self.centralwidget)
self.listWidget.setGeometry(QtCore.QRect(20, 70, 401, 471))
font = QtGui.QFont()
font.setPointSize(12)
self.listWidget.setFont(font)
self.listWidget.setStyleSheet("QListWidget {\n"
" background-color: #c7c3c3;\n"
" color: black; \n"
" border-radius: 7;\n"
"}")
self.listWidget.setObjectName("listWidget")
self.label = QtWidgets.QLabel(self.centralwidget)
self.label.setGeometry(QtCore.QRect(130, 20, 181, 31))
font = QtGui.QFont()
font.setPointSize(20)
font.setBold(False)
font.setItalic(False)
font.setWeight(50)
font.setStrikeOut(False)
font.setKerning(True)
self.label.setFont(font)
self.label.setObjectName("label")
MainWindow.setCentralWidget(self.centralwidget)
self.retranslateUi(MainWindow)
QtCore.QMetaObject.connectSlotsByName(MainWindow)
def retranslateUi(self, MainWindow):
_translate = QtCore.QCoreApplication.translate
MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
self.pushButton.setText(_translate("MainWindow", "Слушать"))
self.pushButton_2.setText(_translate("MainWindow", "Стоп"))
self.label.setText(_translate("MainWindow", "Voice Assistant"))



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
