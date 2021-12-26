# Импортируем необходимые компоненты
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from settings import TG_TOKEN, TG_API_URL


# Функция sms() будет вызвана пользователем при отправке команда /start
# Внутри функции будет описана логика при ее вызове
def sms(bot, update):
    print('Кто-то отправил команду /start. Что мне делать?') # вывод сообщения в консоль для отправки команды /start
    bot.message.reply_text('Здравствуйте, {}!. \n '
                           'Поговорите со мной!' .format(bot.message.chat.first_name))# отправка ответа
# функция parrot() отвечает тем же сообщением, что отправил юзер
def parrot(bot, update):
    print(bot.message.text) # печатаем на экран сообщение пользователя
    bot.message.reply_text(bot.message.text)# отправляем юзеру его же сообщение

# Создаем (объявляем) функцию main, которая будет общаться с Telegram
def main():
    # тело функции, описываем функцию (что она будет делать)
    my_bot = Updater(TG_TOKEN, TG_API_URL, use_context=True)
    my_bot.dispatcher.add_handler(CommandHandler('start',sms))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.text, parrot))
    my_bot.start_polling()# проверка наличия сообщений с платформы Telegram
    my_bot.idle() #бот работает пока его не остановят



# вызываем запуск функции main
main()
