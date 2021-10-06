import peewee as pw

db = pw.SqliteDatabase('database.db')


class User(pw.Model):
    name = pw.CharField()
    best_score = pw.IntegerField()

    class Meta:
        database = db


def initialize_db():
    db.connect()
    db.create_tables([User], safe=True)
    db.close()
