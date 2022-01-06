# Импортируем необходимые компоненты
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters
from settings import TG_TOKEN, TG_API_URL
from handlers import *
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

# Создаем (объявляем) функцию main, которая будет общаться с Telegram
def main():
    # тело функции, описываем функцию (что она будет делать)
    my_bot = Updater(TG_TOKEN, TG_API_URL, use_context=True)
    logging.info('Start Bot')
    my_bot.dispatcher.add_handler(CommandHandler('start', sms))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Покажи мем'), send_meme))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Начать'), sms2))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Расскажи анекдот'), get_anecdote))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.contact, get_contact))# обработчик полученного контакта
    my_bot.dispatcher.add_handler(MessageHandler(Filters.location, get_location))# обработчик полученной геопозиции
    my_bot.dispatcher.add_handler(
        ConversationHandler(entry_points=[MessageHandler(Filters.regex('Заполнить анкету'), anketa_start)],
                            states={
                                    "user_name": [MessageHandler(Filters.text, anketa_get_name)],
                                    "user_age": [MessageHandler(Filters.text, anketa_get_age)],
                                    "evaluation": [MessageHandler(Filters.regex('1|2|3|4|5'), anketa_get_evaluation)],
                                    "comment": [MessageHandler(Filters.regex('Пропустить'), anketa_exit_comment),
                                                MessageHandler(Filters.text, anketa_comment)],
                                    },
                            fallbacks=[MessageHandler(Filters.text | Filters.video | Filters.photo, Filters.document, dontknow)]
                            ))


#    my_bot.dispatcher.add_handler(MessageHandler(Filters.text, parrot))
    my_bot.start_polling()  # проверка наличия сообщений с платформы Telegram
    my_bot.idle()  # бот работает пока его не остановят


# вызываем запуск функции main
if __name__ == "__main__":
    main()