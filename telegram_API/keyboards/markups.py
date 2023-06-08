from telegram import ReplyKeyboardMarkup


def get_genres_markup(genres):
    reply_keyboard = [genres[i:i + 5] for i in range(0, len(genres), 5)]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    return markup
