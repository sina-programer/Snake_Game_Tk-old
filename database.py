import peewee as pw

db = pw.SqliteDatabase('database.db')


class User(pw.Model):
    name = pw.CharField()
    best_score = pw.IntegerField()

    class Meta:
        database = db


if not db.table_exists('User'):
    db.create_tables([User])

import sqlite3
connection = sqlite3.connect('database.db')
print(list(connection.cursor().execute('select * from User')))
connection.close()