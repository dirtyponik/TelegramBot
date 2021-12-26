# Импортируем необходимые компоненты
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from settings import TG_TOKEN, TG_API_URL
from bs4 import BeautifulSoup
import requests


# Функция sms() будет вызвана пользователем при отправке команда /start
# Внутри функции будет описана логика при ее вызове
def sms(bot, update):
    print('Кто-то отправил команду /start. Что мне делать?') # вывод сообщения в консоль для отправки команды /start
    my_keyboard = ReplyKeyboardMarkup([['/start', 'Расскажи анекдот'], ['Кнопка не работает']], resize_keyboard=True)
    bot.message.reply_text('Здравствуйте, {}!. \n '
                           'Поговорите со мной!' .format(bot.message.chat.first_name), reply_markup=my_keyboard) # отправка ответа


def get_anecdote(bot, update):
    receive = requests.get('http://anekdotme.ru/random')# отправка запроса к странице
    page = BeautifulSoup(receive.text, "html.parser") # подключаем HTML парсер для получения текста страницы
    find = page.select('.anekdot_text') # из страницы HTML получаетм class="anekdot_text"
    for text in find:
        page = (text.getText().strip())# Из class="anekdot_text" получаем текст и убираем пробелы по сторонам
    bot.message.reply_text(page)# отправляем один последний анекдот


# функция parrot() отвечает тем же сообщением, что отправил юзер
def parrot(bot, update):
    print(bot.message.text) # печатаем на экран сообщение пользователя
    bot.message.reply_text(bot.message.text)# отправляем юзеру его же сообщение

# Создаем (объявляем) функцию main, которая будет общаться с Telegram
def main():
    # тело функции, описываем функцию (что она будет делать)
    my_bot = Updater(TG_TOKEN, TG_API_URL, use_context=True)
    my_bot.dispatcher.add_handler(CommandHandler('start',sms))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Кнопка не работает'), sms))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Расскажи анекдот'), get_anecdote))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.text, parrot))
    my_bot.start_polling()# проверка наличия сообщений с платформы Telegram
    my_bot.idle() #бот работает пока его не остановят



# вызываем запуск функции main
main()
