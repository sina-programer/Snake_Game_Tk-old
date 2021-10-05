import sqlite3


class Database:
    def __init__(self, file: str = 'database.db'):
        self.database_file = file

    def create_table(self, table: str, columns: tuple):
        self.execute_query(f'CREATE TABLE IF NOT EXISTS {table}({columns})')

    def insert(self, table: str, values: tuple):
        self.execute_query('INSERT INTO ? VALUES ?', (table, values))

    def update(self, table: str, columns, value, row_id):
        self.execute_query('UPDATE ? ?=? WHERE id=?', (table, columns, value, row_id))

    def select_all(self, table: str):
        return self.execute_query('SELECT * FROM ?', (table,))

    def select(self, table: str, row_id: tuple):
        return self.execute_query('SELECT * FROM ? WHERE id=?', (table, row_id))

    def execute_query(self, query, values=None):
        connection = sqlite3.connect(self.database_file)
        cursor = connection.cursor()
        if values:
            result = cursor.execute(query, values)
        else:
            result = cursor.execute(query)
        connection.commit()
        connection.close()

        return result


class Score(Database):
    def __init__(self):
        super(Score, self).__init__()
        self.table_name = 'score'
        self.create_table(self.table_name, ('id INTEGER PRIMARY KEY', 'best_score INTEGER NOT NULL'))

    def insert(self, best_score):
        super(Score, self).insert(self.table_name, best_score)

    def update(self, score_id, best_score):
        super(Score, self).update(self.table_name, ('id', 'best_score'), (best_score,), score_id)

    def select_all(self):
        return super(Score, self).select_all(self.table_name)

    def select(self, score_id):
        return super(Score, self).select(self.table_name, score_id)


class User(Database):
    def __init__(self):
        super(User, self).__init__()
        self.table_name = 'user'
        self.create_table(self.table_name, ('id INTEGER PRIMARY KEY', 'name TEXT NOT NULL'))

    def insert(self, name):
        super(User, self).insert(self.table_name, name)

    def update(self, user_id, name):
        super(User, self).update(self.table_name, ('id', 'name'), (name,), user_id)

    def select_all(self):
        return super(User, self).select_all(self.table_name)

    def select(self, user_id):
        return super(User, self).select(self.table_name, user_id)
