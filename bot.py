# Импортируем необходимые компоненты
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from settings import TG_TOKEN, TG_API_URL
from bs4 import BeautifulSoup
import requests


# Функция sms() будет вызвана пользователем при отправке команда /start
# Внутри функции будет описана логика при ее вызове
def sms(bot, update):
    print('Кто-то отправил команду /start. Что мне делать?')  # вывод сообщения в консоль для отправки команды /start
    bot.message.reply_text('Здравствуйте, {}! \nВыберите ниже, что вам интересно!'
                           .format(bot.message.chat.first_name), reply_markup=get_keyboard())  # отправка ответа

def sms2(bot, update):
        print(
            'Кто-то отправил команду Начать. Что мне делать?')  # вывод сообщения в консоль для отправки команды /start
        bot.message.reply_text('Ну давайте уже начнем, {}! \nВыберите ниже, что вам интересно!'
                               .format(bot.message.chat.first_name), reply_markup=get_keyboard())  # отправка ответа


def get_anecdote(bot, update):
    receive = requests.get('http://anekdotme.ru/random')  # отправка запроса к странице
    page = BeautifulSoup(receive.text, "html.parser")  # подключаем HTML парсер для получения текста страницы
    find = page.select('.anekdot_text')  # из страницы HTML получаетм class="anekdot_text"
    for text in find:
        page = (text.getText().strip())  # Из class="anekdot_text" получаем текст и убираем пробелы по сторонам
    bot.message.reply_text(page)  # отправляем один последний анекдот



# функция parrot() отвечает тем же сообщением, что отправил юзер
#def parrot(bot, update):
#    print(bot.message.text)  # печатаем на экран сообщение пользователя
#    bot.message.reply_text(bot.message.text)  # отправляем юзеру его же сообщение


#функция печатает и отвечает на полученный контакт
def get_contact(bot, update):
    print(bot.message.contact)
    bot.message.reply_text('{}, мы получили ваш номер телефона!'.format(bot.message.chat.first_name))


# функция печатает и отвечает на полученный контакт
def get_location(bot, update):
    print(bot.message.location)
    bot.message.reply_text('{}, мы получили вашу геопозицию!'.format(bot.message.chat.first_name))


# функция создает клавиатуру и ее разметку
def get_keyboard():
    contact_button = KeyboardButton('Отправить контакты', request_contact=True)
    location_button = KeyboardButton('Отправить геопозицию', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([['Начать', 'Расскажи анекдот'], [contact_button, location_button]],resize_keyboard=True)
    return my_keyboard


# Создаем (объявляем) функцию main, которая будет общаться с Telegram
def main():
    # тело функции, описываем функцию (что она будет делать)
    my_bot = Updater(TG_TOKEN, TG_API_URL, use_context=True)
    my_bot.dispatcher.add_handler(CommandHandler('start', sms))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Начать'), sms2))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Расскажи анекдот'), get_anecdote))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.contact, get_contact))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.location, get_location))
#    my_bot.dispatcher.add_handler(MessageHandler(Filters.text, parrot))
    my_bot.start_polling()  # проверка наличия сообщений с платформы Telegram
    my_bot.idle()  # бот работает пока его не остановят


# вызываем запуск функции main
main()
