import sqlite3

from task_manager.config import(
DB_FILE,
SCHEMA_FILE,
DB_TIMEOUT,
SQLITE_JOURNAL_MODE,
)

from contextlib import contextmanager

@contextmanager
def get_db():

    conn = sqlite3.connect(
        DB_FILE,
        timeout=DB_TIMEOUT,
        check_same_thread=False
    )

    conn.row_factory = sqlite3.Row

    try:
        yield conn

    finally:
        conn.close()


def get_connection():

    conn = sqlite3.connect(
        DB_FILE,
        check_same_thread=False
    )

    conn.row_factory = sqlite3.Row

    return conn


def initialize_database():

    conn = get_connection()

    with open(
        SCHEMA_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        conn.executescript(
            f.read()
        )

        conn.execute(
            f"PRAGMA journal_mode={SQLITE_JOURNAL_MODE}"
        )

    conn.commit()

    conn.close()