import os
from pathlib import Path
import re
import sys
import flask_mysqldb

from ..data import databaseHelper

MIGRATION_SCRIPT_VERSION_REGEX = re.compile(r"(\d+)(.*)\.sql")

def migrate():
    """
    Migrates database schema
    """
    current_version = databaseHelper.get_current_db_version()

    schema_path = Path("notes_app") / "sql"
    db = flask_mysqldb.MySQL()

    def version_from_filename(name: str):
        match = MIGRATION_SCRIPT_VERSION_REGEX.match(name)

        if match is None:
            print(f"Bad file name for migration script: {name}", file=sys.stderr)
            return 9999

        version = match.group(1)
        return int(version)


    # (filename, version) pair
    files = [
        (filename, version_from_filename(filename))
        for filename in os.listdir(schema_path)
    ]

    # Filter out migrations based on current db version
    # FIXME: Can we optimize this?
    files = [
        file for file in files
        if file[1] > current_version
    ]

    # Sort by version
    files.sort(key = lambda file: file[1])

    for filename, version in files:
        try:
            with db.connection.cursor() as cursor:
                print(f"Running migration: {filename} ({version})", end="")
                with open(schema_path / filename) as fp:
                    sql = fp.read()
                cursor.execute(sql)
            print(".....OK")
        except Exception as e:
            print(".....FAILED")
            raise e  # re-raise
    
    db.connection.commit()

    if files:
        # determine the latest migration version we applied
        updated_version = files[-1][1]
        databaseHelper.update_db_version(updated_version)
        print(f"Migrated database to version {updated_version}")
    else:
        print("No migrations to apply")

def purge():
    """
    Drop all the tables from database
    """
    tables = (
        "database_version",
        "notes",
        "users",
    )

    db = flask_mysqldb.MySQL()

    for table in tables:
        print(f"Dropping table {table}")
        with db.connection.cursor() as cursor:
            cursor.execute(f"DROP TABLE IF EXISTS {table}")
