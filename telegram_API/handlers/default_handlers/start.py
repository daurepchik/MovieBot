import logging

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from database.db_core import crud

start_logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обрабатывает команду 'start' и отправляет приветственное сообщение пользователю.
    Записывает отправленный запрос в таблицу Историй
    :param update: Входящее обновление от Telegram.
    :type update: Update
    :param context: Контекстный объект, предоставленный библиотекой `python-telegram-bot`.
    :type context: ContextTypes.DEFAULT_TYPE
    :return: None
    """
    user = update.effective_user
    start_data = {'command': 'start'}
    crud.insert_history_data(update.effective_user, start_data)
    await update.message.reply_text(f'''Hey {user.first_name}!

I am your personal Telegram bot and I am here to help you with movies! I'm using an amazing 3rd party API,
which gives me access to a huge movie database.

My main function is to provide information about the Top 250 movies by rating, according to IMDB ranking.

To find out which commands I support, just type /help,
and I will tell you more about how to interact with me and enjoy the world of cinema!''')


start_command_handler = CommandHandler("start", start_command)
