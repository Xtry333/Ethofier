import settings as s
from telegram import Bot
from datetime import datetime

bot = Bot(s.BOT_TOKEN)


def log_message(text):
    time = datetime.now().strftime(s.DATETIME_FORMAT)
    msg = '*[Ethofier App]* ' + time + '``` ' + text + '```'
    bot.send_message(s.DEBUG_CHAT_ID, msg, parse_mode='Markdown', disable_notification=True)


def send_notification(id, title, link):
    msg = '*' + title + '*\n' + link
    bot.send_photo(
        s.NOTIFICATIONS_CHAT_ID,
        caption=msg,
        photo=s.THUMBNAIL_URL % id,
        parse_mode='Markdown')


def send_simple_notification(id, title, link):
    msg = '*' + title + '*\n' + link
    bot.send_message(
        s.NOTIFICATIONS_CHAT_ID, msg,
        parse_mode='Markdown')

# log_message('Hello there. Up and running!')
