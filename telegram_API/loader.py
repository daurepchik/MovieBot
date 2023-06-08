import logging

from telegram.ext import Application

from settings import ApplicationSettings
from telegram_API.handlers.custom_handlers import low, high, custom, history
from telegram_API.handlers.default_handlers import start, help

app_settings = ApplicationSettings()

bot_loader_logger = logging.getLogger(__name__)


def load_bot() -> None:
    application = Application.builder().token(app_settings.telegram_bot_api_key.get_secret_value()).build()

    application.add_handler(start.start_command_handler)
    application.add_handler(help.help_command_handler)
    application.add_handler(high.high_command_handler)
    application.add_handler(low.low_command_handler)
    application.add_handler(custom.custom_command_handler)
    application.add_handler(history.history_command_handler)

    application.run_polling()
