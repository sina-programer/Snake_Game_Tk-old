import peewee as pw

db = pw.SqliteDatabase('database.db')

class User(pw.Model):
    name = pw.CharField()
    best_score = pw.IntegerField()

    class Meta:
        database = db
