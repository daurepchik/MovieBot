import logging

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from database.db_core import crud

history_logger = logging.getLogger(__name__)


async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обрабатывает команду "history" и извлекает историю команд пользователя.
    :param update: Входящее обновление.
    :param context: Контекст бота.
    :return: None
    """
    history = crud.retrieve_history(update.effective_user)
    history_row_count = history.count()
    command_plural = 's' if history_row_count > 1 else ''
    history_message = f'Here are last {history_row_count} command{command_plural} that you entered:\n'
    for i, record in enumerate(history, start=1):
        history_message += f'{i}. /{record.command}\n'
        if record.command == 'custom':
            history_message += f'{" " * 4}Genre: {record.genre}, ' \
                               f'Start Year: {record.start_year}, ' \
                               f'End Year: {record.end_year}\n'
        elif record.command in ('high', 'low'):
            history_message += f'{" " * 4}Genre: {record.genre}\n'
    await update.message.reply_text(history_message)


history_command_handler = CommandHandler('history', history_command)
