from datetime import datetime

import peewee as pw

db = pw.SqliteDatabase('history.db')


class BaseModel(pw.Model):
    create_datetime = pw.DateTimeField(default=datetime.now)

    class Meta:
        database = db


class BotUser(BaseModel):
    id = pw.IntegerField(primary_key=True)
    username = pw.CharField(null=True, default=None)
    first_name = pw.CharField(null=True, default=None)


class History(BaseModel):
    user = pw.ForeignKeyField(BotUser, backref='history')
    command = pw.TextField()
    genre = pw.CharField(null=True, default=None)
    start_year = pw.IntegerField(null=True, default=None)
    end_year = pw.IntegerField(null=True, default=None)
