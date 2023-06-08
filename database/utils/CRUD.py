import logging
from typing import Dict, TypeVar

import peewee as pw
from telegram import User

from database.models import db, BotUser, History

crud_logger = logging.getLogger(__name__)

T = TypeVar("T")


class CRUDInterface:
    """CRUD Interface class for easier database access"""

    @staticmethod
    def insert_history_data(user: User, data: Dict) -> None:
        """
        Inserts history data into the database for the specified user.
        :param user: The Telegram user object.
        :param data: The data to be inserted.
        :return: None
        """
        try:
            crud_logger.info(f'Inserting "{data["command"]}" history for @{user.username}')
            with db.atomic():
                user_info = {
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                }
                user_obj, is_created = BotUser.get_or_create(**user_info)
                History.create(user=user_obj, **data)
            crud_logger.debug(f'OK. Inserted "{data["command"]}" history for @{user.username}')
        except pw.PeeweeException as e:
            crud_logger.exception(f'Something went wrong during history insertion. Error: {e}')

    @staticmethod
    def retrieve_history(user: User) -> pw.ModelSelect:
        """
        Retrieves history data from the database for the specified user.
        :param user: The Telegram user object.
        :return: A query object representing the retrieved history data.
        """
        try:
            crud_logger.info(f'Retrieving history for @{user.username}')
            with db.atomic():
                user_info = {
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                }
                user_obj, is_created = BotUser.get_or_create(**user_info)
                response = History.select() \
                    .where(History.user == user_obj) \
                    .order_by(History.create_datetime.desc()) \
                    .limit(10)
            crud_logger.debug(f'OK. Retrieved history for @{user.username}')
            return response
        except pw.PeeweeException as e:
            crud_logger.exception(f'Something went wrong during history retrieval. Error: {e}')
