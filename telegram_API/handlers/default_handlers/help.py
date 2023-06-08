import logging

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from database.db_core import crud

help_logger = logging.getLogger(__name__)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обрабатывает команду 'help' и предоставляет список доступных команд и помощь.
    Записывает отправленный запрос в таблицу Историй
    :param update: Входящее обновление от Telegram.
    :param context: Контекстный объект, предоставленный библиотекой `python-telegram-bot`.
    :return: None
    """
    help_data = {'command': 'help'}
    crud.insert_history_data(update.effective_user, help_data)
    await update.message.reply_text(f'''/start - Start the bot and initiate interaction.
/help - Get a list of commands and assistance.
/low - Get the oldest movies in the top.
/high - Get the newest movies in the top.
/custom - Get movies within custom range in the top.
/history - View the history of user requests.
Feel free to use these commands to explore movie ratings and enjoy the experience!''')


help_command_handler = CommandHandler("help", help_command)
