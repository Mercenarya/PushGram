import sqlite3
import os



current = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(current,"telegram-trans.db")
DB = sqlite3.connect("telegram-trans.db",check_same_thread=False)
cursor = DB.cursor()

print(db_path)


def Note():
    setNote = '''
        CREATE TABLE note (
            title VARCHAR(900) PRIMARY KEY,
            textiled TEXT
        )
    '''
    return setNote
try:
    if sqlite3.Connection:
        print("Connection set up")
        cursor.execute(Note())
       
        DB.commit()
    elif sqlite3.Error:
        print("DB Error")
except sqlite3.Error as error:
    print(error)