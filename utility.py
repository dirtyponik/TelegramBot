# Импортируем необходимые компоненты
from telegram import ReplyKeyboardMarkup, KeyboardButton

SMILE = ['😊', '😀', '😇', '🤠', '😎', '🤓', '👶', '🧑‍🚀', '👮', '🦸', '🧟', 'grinning face']
CALBACK_BUTTON_PICTURE = "Покажи мем 🏞"
CALBACK_BUTTON_PEN = "Заполнить анкету 🖌"
CALBACK_BUTTON_START = "Начать 🎰"
CALBACK_BUTTON_JOKE = "Расскажи анекдот 🎭"


# функция создает клавиатуру и ее разметку
def get_keyboard():
   contact_button = KeyboardButton('Отправить контакты', request_contact=True)
   location_button = KeyboardButton('Отправить геопозицию', request_location=True)
   my_keyboard = ReplyKeyboardMarkup([[CALBACK_BUTTON_START, CALBACK_BUTTON_JOKE], [contact_button, location_button], [CALBACK_BUTTON_PEN, CALBACK_BUTTON_PICTURE]], resize_keyboard=True)
   return my_keyboard
