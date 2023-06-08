import logging

from database.db_core import init_db
from telegram_API.loader import load_bot

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

main_logger = logging.getLogger(__name__)

if __name__ == "__main__":
    main_logger.info('Initiating DB')
    init_db()
    main_logger.info('Loading the bot')
    load_bot()
