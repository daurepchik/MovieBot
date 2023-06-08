import logging
from datetime import datetime

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

custom_logger = logging.getLogger(__name__)

GENRE_CHOOSE, YEAR_START, YEAR_END, MOVIE_COUNT = range(4)

genres = site_api_interface.get_genres_list()
markup = get_genres_markup(genres)


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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


async def movie_year_start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Получает от пользователя год выпуска фильмов с которого начать поиск и сохраняет выбранный год в контексте.
    :param update: Входящее обновление.
    :param context: Контекст бота.
    :return: Следующее состояние после обработки команды.
    """
    genre = update.message.text
    context.user_data["genre"] = genre if genre != 'All' else None
    await update.message.reply_text(f"Movies start year?", reply_markup=ReplyKeyboardRemove())
    return YEAR_START


async def wrong_movie_year_start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Уведомляет пользователя о некорректном годе выпуска фильма и просит повторить попытку.
    :param update: Входящее обновление.
    :param context: Контекст бота.
    :return: Следующее состояние после обработки команды.
    """
    await update.message.reply_text(
        f'''Year should be the integer from 1900 to {datetime.now().year}. 
Please try again.
Movies start year?''')
    return YEAR_START


async def movie_year_end_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Получает от пользователя год выпуска фильмов с которого закончить поиск и сохраняет выбранный год в контексте.
    :param update: Входящее обновление.
    :param context: Контекст бота.
    :return: Следующее состояние после обработки команды.
    """
    start_year = update.message.text
    context.user_data["start_year"] = start_year
    await update.message.reply_text(f"Movies end year?")
    return YEAR_END


async def wrong_movie_year_end_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Уведомляет пользователя о некорректном годе выпуска фильма и просит повторить попытку.
    :param update: Входящее обновление.
    :param context: Контекст бота.
    :return: Следующее состояние после обработки команды.
    """
    await update.message.reply_text(
        f'''Year should be the integer from 1900 to {datetime.now().year}. 
Please try again.
Movies end year?''')
    return YEAR_END


async def movie_count_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Получает от пользователя кол-во фильмов и сохраняет выбранное кол-во в контексте.
    :param update: Входящее обновление.
    :param context: Контекст бота.
    :return: Следующее состояние после обработки команды.
    """
    end_year = update.message.text
    context.user_data["end_year"] = end_year
    await update.message.reply_text(f"Movie count from 1 to 10?")

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
    """Получает от пользователя количество фильмов и запрашивает информацию о фильмах
    с выбранным жанром и количеством и промежутком годов.
    Отправляет информацию о фильмах в виде ответов на сообщение пользователя.
    Записывает отправленный запрос в таблицу Историй
    :param update: Входящее обновление.
    :param context: Контекст бота.
    :return: Следующее состояние после обработки команды.
    """
    movie_count = update.message.text
    genre = context.user_data['genre']
    start_year = context.user_data['start_year']
    end_year = context.user_data['end_year']
    custom_data = {'command': 'custom', 'genre': genre, 'start_year': start_year, 'end_year': end_year}
    crud.insert_history_data(update.effective_user, custom_data)
    movies = site_api_interface.get_movies_custom(genre, movie_count, min(start_year, end_year),
                                                  max(start_year, end_year))
    if not movies:
        custom_logger.error(f'"{genre}" movies do not exist in the top :(')
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
custom_command_handler = ConversationHandler(
    entry_points=[CommandHandler("custom", custom_command)],
    states={
        GENRE_CHOOSE: [
            MessageHandler(filters.Regex(genres_regex), movie_year_start_handler),
            MessageHandler(~filters.Regex(genres_regex), wrong_genre_handler)
        ],
        YEAR_START: [
            MessageHandler(filters.Regex('^[12][90][0129]\d$'), movie_year_end_handler),
            MessageHandler(~filters.Regex('^[12][90][0129]\d$'), wrong_movie_year_start_handler)
        ],
        YEAR_END: [
            MessageHandler(filters.Regex('^[12][90][0129]\d$'), movie_count_handler),
            MessageHandler(~filters.Regex('^[12][90][0129]\d$'), wrong_movie_year_end_handler)
        ],
        MOVIE_COUNT: [
            MessageHandler(filters.Regex(r'^([1-9]|10)$'), movie_info_reply),
            MessageHandler(~filters.Regex(r'^([1-9]|10)$'), wrong_movie_count_handler)
        ]
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)
