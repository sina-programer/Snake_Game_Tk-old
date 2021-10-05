import sqlite3


class Database:
    def __init__(self, file:str='database.db'):
        self.database_file = file
        
    def create_table(self, table:str, columns:tuple):
        self.execute_query(f'CREATE TABLE IF NOT EXISTS {table}({",\n".join(columns)})')

    def insert(self, table:str, values:tuple):
        self.execute_query(f'INSERT INTO {table} VALUES ({", ".join(values)})')
    
    def update(self, table:str, column:str, value, score_id):
        self.execute_query(f'UPDATE {table} {column}={value} WHERE id={score_id}')
    
    def select_all(self, table:str):
        return self.execute_query(f'SELECT * FROM {table}')
    
    def select(self, table:str, columns:tuple):
        return self.execute_query(f'SELECT {",".join(columns)} FROM {table}')
    
    def execute_query(query):
        connection = sqlite3.connect(self.database_file)
        cursor = connection.cursor()
        result = cursor.execute(query)
        connection.commit()
        connection.close()
        
        return result
