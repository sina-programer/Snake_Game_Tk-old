import peewee as pw

db = pw.SqliteDatabase('database.db')
db.connect()

class User(pw.Model):
    name = pw.CharField()
    best_score = pw.IntegerField()
    
    @staticmethod
    def connect():
        db.connect()
        
    @staticmethod
    def close():
        db.close()

    class Meta:
        database = db

if not db.table_exists('User'):
    db.create_tables([User])
