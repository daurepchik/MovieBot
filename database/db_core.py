from database.models import db, History, BotUser
from database.utils.CRUD import CRUDInterface


def init_db():
    with db:
        db.create_tables([History, BotUser])


crud = CRUDInterface()
