import logging
import random

from datetime import datetime

from scrap_keys import keys_parse
from config import KEYS_SITE, HEADERS

from telegram import Bot, Update
from telegram.ext import Updater, Filters, CommandHandler, MessageHandler

from config import TG_TOKEN
from config import TG_API_URL

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

lang = ''


def do_start(bot: Bot, update: Update):
    lang = update.message.from_user.language_code
    text = 'Hello! Print /key and take HideMy.name VPN key\n(24 hours)!' if lang == 'en' \
        else 'Привет! Напиши /key и получи ключ для HideMy.name\n(24 часа)'
    bot.sendMessage(
        chat_id=update.message.chat_id,
        text=text
    )


def do_key(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    time, keys = keys_parse(KEYS_SITE, HEADERS)
    key = random.choice(keys)
    # format_keys = ''
    # for i, key in enumerate(keys):
    # format_keys += ('%s.  [ %s ]\n' % (i + 1, keys[i]))
    text = ('Key was updated %s\n\n' % time) if lang == 'en' \
        else ('Ключ был обновлен %s\n\n' % time)
    time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    print(update.message.from_user.username + '\n', key + '\n', time)
    bot.sendMessage(
        chat_id=chat_id,
        text=text
    )
    bot.sendMessage(
        chat_id=chat_id,
        text=key
    )


def do_echo(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    name: str = update.message.chat.username
    text = ('Sorry, %s, but I can give you VPN key only...' % name)
    bot.sendMessage(
        chat_id=chat_id,
        text=text
    )


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


if __name__ == '__main__':
    bot = Bot(
        token=TG_TOKEN,
        base_url=TG_API_URL,
    )
    updater = Updater(
        bot=bot,
    )

    start_handler = CommandHandler(['start', 'help'], do_start)
    key_handler = CommandHandler('key', do_key)
    message_handler = MessageHandler(Filters.text, do_echo)

    dp = updater.dispatcher
    dp.add_handler(start_handler)
    dp.add_handler(key_handler)
    dp.add_handler(message_handler)
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()
