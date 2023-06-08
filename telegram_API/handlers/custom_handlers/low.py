import logging

from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from database.db_core import crud
from site_API.site_api import site_api_interface
from telegram_API.keyboards.markups import get_genres_markup
from telegram_API.utils.command_handlers_util import reply_movie_info

low_logger = logging.getLogger(__name__)

GENRE_CHOOSE, MOVIE_COUNT = range(2)

genres = site_api_interface.get_genres_list()
markup = get_genres_markup(genres)


async def low_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Запрашивает у пользователя выбор жанра из предоставленной клавиатуры.
    :param update: Входящее обновление.
    :param context: Контекст бота.
    :return: Следующее состояние после обработки команды.
    """
    await update.message.reply_text(
        "Choose Genre:",
        reply_markup=markup,
    )
    return GENRE_CHOOSE


async def wrong_genre_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Уведомляет пользователя о выборе некорректного жанра и просит выбрать правильную опцию.
    :param update: Входящее обновление.
    :param context: Контекст бота.
    :return: Следующее состояние после обработки команды.
    """
    await update.message.reply_text(
        '''Wrong genre selected. Please select the correct option from the keyboard.
Choose Genre:''',
        reply_markup=markup,
    )
    return GENRE_CHOOSE


async def movie_count_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Получает от пользователя количество фильмов и сохраняет выбранный жанр в контексте.
    :param update: Входящее обновление.
    :param context: Контекст бота.
    :return: Следующее состояние после обработки команды.
    """
    genre = update.message.text
    context.user_data["genre"] = genre if genre != 'All' else None
    await update.message.reply_text(f"Movie count from 1 to 10?", reply_markup=ReplyKeyboardRemove())

    return MOVIE_COUNT


async def wrong_movie_count_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Уведомляет пользователя о некорректном количестве фильмов и просит повторить попытку.
    :param update: Входящее обновление.
    :param context: Контекст бота.
    :return: Следующее состояние после обработки команды.
    """
    await update.message.reply_text(
        '''The minimum allowed number is 1, the maximum is 10. 
Please try again.
Movie count from 1 to 10?''')
    return MOVIE_COUNT


async def movie_info_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Получает от пользователя количество фильмов и запрашивает информацию о фильмах с выбранным жанром и количеством.
    Отправляет информацию о фильмах в виде ответов на сообщение пользователя.
    Записывает отправленный запрос в таблицу Историй
    :param update: Входящее обновление.
    :param context: Контекст бота.
    :return: Следующее состояние после обработки команды.
    """
    genre = context.user_data['genre']
    movie_count = update.message.text
    low_data = {'command': 'low', 'genre': genre}
    crud.insert_history_data(update.effective_user, low_data)
    movies = site_api_interface.get_movies_low(genre, movie_count)
    if not movies:
        low_logger.error(f'"{genre}" movies do not exist in the top :(')
        await update.message.reply_text(f'"{genre}" movies do not exist in the top :(')
        return ConversationHandler.END
    await reply_movie_info(update, context, movies)

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Отправляет пользователю прощальное сообщение и очищает пользовательские данные.
    :param update: Входящее обновление.
    :param context: Контекст бота.
    :return: Следующее состояние после обработки команды.
    """
    await update.message.reply_text(f'Good Bye')
    context.user_data.clear()

    return ConversationHandler.END


genres_regex = '(' + '|'.join(genres) + ')'
low_command_handler = ConversationHandler(
    entry_points=[CommandHandler("low", low_command)],
    states={
        GENRE_CHOOSE: [
            MessageHandler(filters.Regex(genres_regex), movie_count_handler),
            MessageHandler(~filters.Regex(genres_regex), wrong_genre_handler)
        ],
        MOVIE_COUNT: [
            MessageHandler(filters.Regex(r'^([1-9]|10)$'), movie_info_reply),
            MessageHandler(~filters.Regex(r'^([1-9]|10)$'), wrong_movie_count_handler)
        ]
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)
