import sqlite3


def execute_query(query, args=None):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    result = cursor.execute(query, args)
    connection.commit()
    connection.close()
    return result


def create_table():
    execute_query('''CREATE TABLE IF NOT EXISTS score(
        id INTEGER PRIMARY KEY,
        best_score INTEGER NOT NULL
    )''')


def add_score(best_score: int):
    execute_query('INSERT INTO score VALUES (NULL, ?)', (best_score,))


def delete_score(score_id: int):
    execute_query('DELETE FROM score WHERE id=?', (score_id,))


def update_score(score_id: int, best_score: int):
    execute_query('UPDATE score best_score=? WHERE id=?', (best_score, score_id))


def view_score():
    return execute_query('SELECT * FROM score')


def add_or_update(best_score: int):
    """
    Work on score table.
    This function check if "the best score exist" in database update this
    and if not exist add it to database.

    :param best_score:
    :return:
    """

    execute_query('''
        IF EXIST (SELECT * FROM score WHERE best_score=?)
        BEGIN
        UPDATE score best_score=? WHERE best_score=?
        END
        ELSE
        BEGIN
        INSERT INTO score VALUES (NULL, ?)
        END
    ''', (best_score, best_score, best_score, best_score))


def add_or_update_with_id(score_id: int, best_score: int):
    """
    Work on score table.
    This function check if score_id exist in database update it and
    if not exist add it to database.
    :param score_id:
    :param best_score:
    :return:
    """

    execute_query('''
        IF EXIST (SELECT * FROM score WHERE id=?)
        BEGIN
        UPDATE score best_score=? WHERE id=?
        END
        ELSE
        BEGIN
        INSERT INTO score VALUES (NULL, ?)
        END
    ''', (score_id, best_score, score_id, best_score))


create_table()
