import os

from dotenv import load_dotenv, find_dotenv
from pydantic import BaseSettings, SecretStr, StrictStr

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()


class ApplicationSettings(BaseSettings):
    # Site Settings
    site_api_key: SecretStr = os.getenv("SITE_API_KEY", None)
    site_api_host: StrictStr = os.getenv("SITE_API_HOST", None)

    # Telegram Bot settings
    telegram_bot_api_key: SecretStr = os.getenv("TELEGRAM_BOT_API_KEY", None)
