from typing import List, Dict

from telegram import Update
from telegram.error import BadRequest
from telegram.ext import ContextTypes


async def reply_movie_info(update: Update, context: ContextTypes.DEFAULT_TYPE, movies: List[Dict]) -> None:
    """
    Отправляет информацию о фильмах в ответ на сообщение пользователя.
    :param update: Входящее обновление.
    :param context: Контекст бота.
    :param movies: Список фильмов
    :return: None
    """
    for movie in movies:
        try:
            await update.message.reply_photo(movie['image_url'], caption=movie['image_caption'])
        except BadRequest:
            await update.message.reply_document(movie['image_url'], caption=movie['image_caption'])

        reply_text = f'''
Movie title: {movie['title']}
Movie position: {movie['position']}
Movie release date: {movie['release_date']}'''
        await update.message.reply_text(reply_text)
    context.user_data.clear()
