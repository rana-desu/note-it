from typing import Optional
from flask_mysqldb import MySQL
import MySQLdb
from MySQLdb.constants import ER

from .models import User
from .models import Note

MYSQL_ERROR_CODE_NO_SUCH_TABLE = 1146

db = MySQL()  

def init(app):
    db.__init__(app)

# authentication and authorisation
def register_user(username, email, password):
    with db.connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO users(username, email, password_hash) VALUES(%s, %s, %s)",
            (username, email, password))

        db.connection.commit()

def fetch_user_by_id(user_id: int) -> Optional[User]:
    with db.connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()

    if result is not None:
        return User(**result)

def fetch_user_by_email(email: str) -> User:
    with db.connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        result = cursor.fetchone()

    if result is not None:
        return User(**result)

def is_email_available(email: str) -> bool:
    """
    Checks if the given email is available for registration for a new user
    i.e. the email has not been previously used to create an account.
    """
    with db.connection.cursor() as cursor:
        cursor.execute(
            "SELECT EXISTS(SELECT user_id FROM users WHERE email = %s)",
            (email,))

        _, exists = cursor.fetchone().popitem()
        return not exists

# MySQL queries for operation on notes
def insert_note(owner_id, title, desc):
    with db.connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO notes(owner_id, title, description) VALUES(%s, %s, %s)", 
            (owner_id, title, desc))
        db.connection.commit()

def all_notes(owner_id) -> tuple[Note]:
    with db.connection.cursor() as cursor:
        cursor.execute("SELECT * FROM notes where owner_id = %s", (owner_id,))
        result = cursor.fetchall()

    return tuple(Note(**row) for row in result)

def fetch_note(note_id) -> Note:
    with db.connection.cursor() as cursor:
        cursor.execute("SELECT * FROM notes WHERE note_id = %s", (note_id,))
        result = cursor.fetchall()

        print(tuple(Note(**row) for row in result))
    
    return tuple(Note(**row) for row in result)

def edit_note(title, desc, note_id):
    with db.connection.cursor() as cursor:
        cursor.execute(
            "UPDATE notes SET title = %s, description = %s WHERE note_id = %s", 
            (title, desc, note_id))
        
        db.connection.commit()

def delete_note(note_id, owner_id):
    with db.connection.cursor() as cursor:
        cursor.execute("DELETE FROM notes WHERE note_id = %s and owner_id = %s", (note_id, owner_id))
        db.connection.commit()

# Migration
def get_current_db_version() -> int:
    with db.connection.cursor() as cursor:
        try:
            cursor.execute("SELECT database_version FROM database_version")
        except MySQLdb.ProgrammingError as e:
            if e.args and e.args[0] == ER.NO_SUCH_TABLE:
                return -1  # return -1 when db version table does not exist
            raise e  # re-raise

        return cursor.fetchone()["database_version"]

def update_db_version(version: int):
    with db.connection.cursor() as cursor:
        cursor.execute("REPLACE INTO database_version(database_version) VALUES(%s)", (version,))
        db.connection.commit()
