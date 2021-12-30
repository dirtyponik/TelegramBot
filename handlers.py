# Импортируем необходимые компоненты
from bs4 import BeautifulSoup
from glob import glob
from random import choice
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, ParseMode
from telegram.ext import ConversationHandler

from utility import get_keyboard
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

#функция оправляет случайную картинку
def send_meme(bot, update):
    lists = glob('images/*')#создаем список из названий картинок
    picture = choice(lists)#берем из списка одну картинку
    update.bot.send_photo(chat_id=bot.message.chat.id, photo=open(picture, 'rb'))#отправляем картинку


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


def anketa_start(bot, update):
    bot.message.reply_text('Как вас зовут?', reply_markup=ReplyKeyboardRemove())
    return "user_name"

def anketa_get_name(bot, update):
    update.user_data['name'] = bot.message.text # временно сохраняем ответ
    bot.message.reply_text("Сколько вам лет?") # задаем вопрос
    return "user_age" # ключ для определения следующего шага


def anketa_get_age(bot, update):
    update.user_data['age'] = bot.message.text  # временно сохраняем ответ
    reply_keyboard = [["1", "2", "3", "4", "5"]]# создаем клавиатуру
    bot.message.reply_text(
        "Оцените статью от 1 до 5",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)) #при нажатии клавиатура исчезает
    return "evaluation" #ключ для определения следующего шага


def anketa_get_evaluation(bot, update):
    update.user_data['evaluation'] = bot.message.text  # временно сохраняем ответ
    reply_keyboard = [["Пропустить"]]  # создаем клавиатуру
    bot.message.reply_text("Напишите отзыв или нажмите кнопку пропустить этот шаг.",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True))  # при нажатии клавиатура исчезает
    return "comment"  # ключ для определения следующего шага


def anketa_comment(bot, update):
    update.user_data['comment'] = bot.message.text # временно сохраняем ответ
    text = """Результат опроса:
    <b>Имя:</b> {name}
    <b>Возраст:</b> {age}
    <b>Оценка:</b> {evaluation}
    <b>Комментарий:</b> {comment}""".format(**update.user_data)
    bot.message.reply_text(text, parse_mode=ParseMode.HTML)# формирование текстового сообщения с форматированием HTML
    bot.message.reply_text("Спасибо вам за комментарий!", reply_markup=get_keyboard()) # сообщение и возврат основной клавиатуры
    return ConversationHandler.END #выход из диалога



def anketa_exit_comment(bot, update):
    update.user_data['comment'] = bot.message.text  # временно сохраняем ответ
    text = """Результат опроса:
        <b>Имя:</b> {name}
        <b>Возраст:</b> {age}
        <b>Оценка:</b> {evaluation)""".format(**update.user_data)
    bot.message.reply_text(text, parse_mode=ParseMode.HTML)  # формирование текстового сообщения с форматированием HTML
    bot.message.reply_text("Спасибо!", reply_markup=get_keyboard())  # сообщение и возврат основной клавиатуры
    return ConversationHandler.END  # выход из диалога

def dontknow(bot, update):
    bot.message.reply_text("Я вас не понимаю, выберите оценку на клавиатуре!")

