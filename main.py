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


logger = logging.getLogger()
logging_format = '%(asctime)s : %(name)s : %(levelname)s : %(message)s'
logging.basicConfig(
    level=logging.INFO,
    format=logging_format
)
fh = logging.FileHandler(
    "logs.log",
    encoding='utf-8'
)
fh.setFormatter(logging.Formatter(logging_format))
logger.addHandler(fh)


try:
    bot = telebot.TeleBot(
        token=os.getenv("BOT_TOKEN"),
        parse_mode='html',
        disable_web_page_preview=True
    )
except:
    logger.critical(traceback.format_exc())
    os._exit(0)


def send_logs(id: int):
    if not isinstance(id, int):
        return
    
    if os.path.exists("logs.log"):
        try:
            with open("logs.log", "rb") as file:
                bot.send_document(id, file)
        except:
            logger.error(traceback.format_exc())

if os.getenv("LOGS_CHAT_ID"):
    send_logs(os.getenv("LOGS_CHAT_ID"))


@bot.message_handler(commands=['get_logs', 'logs', 'log'], chat_types=['private'])
def logs_command(message: types.Message):
    if message.from_user.id != os.getenv("ADMIN_ID"):
        return

    send_logs(message.from_user.id)


@bot.channel_post_handler(content_types=["pinned_message"])
def delete_pinned_messagess(message: types.Message):
    try:
        bot.delete_message(message.chat.id, message.id, timeout=10)
    except telebot.apihelper.ApiTelegramException:
        logger.error(f"Chat: {message.chat} | " + str(traceback.format_exc()))
    except:
        logger.error(f"Chat: {message.chat} | " + str(traceback.format_exc()))


@bot.message_handler(content_types=["pinned_message", "new_chat_members"])
def delete_pinned_messagess_chat(message: types.Message):
    try:
        bot.delete_message(message.chat.id, message.id, timeout=10)
    except telebot.apihelper.ApiTelegramException:
        logger.error(f"Chat: {message.chat} | " + str(traceback.format_exc()))
    except:
        logger.error(f"Chat: {message.chat} | " + str(traceback.format_exc()))


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
