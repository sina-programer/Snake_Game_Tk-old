import peewee as pw

db = pw.SqliteDatabase('database.db')
db.connect()


class User(pw.Model):
    name = pw.CharField(unique=True)
    snake_head_color = pw.CharField(7)
    snake_body_color = pw.CharField(7)

    class Meta:
        database = db


class Score(pw.Model):
    user = pw.ForeignKeyField(User)
    best_score = pw.IntegerField()
    level_of_best_score = pw.IntegerField()

    class Meta:
        database = db


# Create tables
not db.table_exists('User') and db.create_tables([User])
not db.table_exists('Score') and db.create_tables([Score])
