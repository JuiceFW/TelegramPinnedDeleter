import traceback
import logging
import time
import os

from dotenv import load_dotenv
from telebot import types
import telebot

load_dotenv()


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
os.chdir(BASE_DIR)


try:
    bot = telebot.TeleBot(
        token=os.getenv("BOT_TOKEN"),
        parse_mode='html',
        disable_web_page_preview=True
    )
except:
    print(traceback.format_exc())
    logging.critical(traceback.format_exc())
    os._exit(0)


@bot.channel_post_handler(content_types=["pinned_message"])
def delete_pinned_messagess(message: types.Message):
    try:
        bot.delete_message(message.chat.id, message.id, timeout=10)
    except telebot.apihelper.ApiTelegramException:
        logging.critical(f"Chat: {message.chat} | " + str(traceback.format_exc()))
    except:
        print(traceback.format_exc())
        logging.critical(f"Chat: {message.chat} | " + str(traceback.format_exc()))


@bot.message_handler(content_types=["pinned_message", "new_chat_members"])
def delete_pinned_messagess_chat(message: types.Message):
    try:
        bot.delete_message(message.chat.id, message.id, timeout=10)
    except telebot.apihelper.ApiTelegramException:
        logging.critical(f"Chat: {message.chat} | " + str(traceback.format_exc()))
    except:
        print(traceback.format_exc())
        logging.critical(f"Chat: {message.chat} | " + str(traceback.format_exc()))


@bot.message_handler(commands=["start", "help", "menu"], chat_types=["private"])
def start_message(message: types.Message):
    bot.send_message(message.chat.id, "Привет! Спасибо, что выбрали этого бота!\n\n<b>Данный бот удаляет системные сообщения телеграмма из канала. Чтобы бот начал рабоать - просто добавьте его к себе в канал/чат и выдайте ему права администратора!</b>\n\n<i>made by Juice</i>")


while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except:
        print(traceback.format_exc())
        logging.critical(traceback.format_exc())
        time.sleep(10)
