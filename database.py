import peewee

db = peewee.SqliteDatabase('database.db')


class User(peewee.Model):
    name = peewee.CharField()

    class Meta:
        database = db


class Score(peewee.Model):
    best_score = peewee.IntegerField()
    user = peewee.ForeignKeyField(User)

    class Meta:
        database = db
