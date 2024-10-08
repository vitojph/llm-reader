import os
import sqlite3
import sys
from datetime import datetime, timedelta
from typing import List

from llm_reader.page import Page

dbname = "llm-reader.db"


def serialize_categories(categories: List) -> str:
    if not categories:
        return ""
    elif isinstance(categories, list):
        return ", ".join(categories)
    else:
        return str(categories)


def add_page(p: Page) -> None:
    if not os.path.isfile(dbname):
        print(f"Cannot find {dbname} database. Run create-db.py first.")
        sys.exit()

    try:
        con = sqlite3.connect(dbname)
        cur = con.cursor()

        exists_query = "SELECT id FROM pages WHERE url = ?;"
        cur.execute(exists_query, (p.url,))
        result = cur.fetchone()

        if result is None:
            insert_query = """INSERT INTO pages
            ('id', 'title', 'url', 'summary', 'user', 'categories', 'created_at')
            VALUES (?, ?, ?, ?, ?, ?, ?);"""

            now = datetime.now()
            categories = serialize_categories(p.categories)
            row = (None, p.title, p.url, p.summary, "vitojph", categories, now)
            cur.execute(insert_query, row)
            con.commit()
    except sqlite3.Error as err:
        print(f"Error: {err}")
    finally:
        if con:
            con.close()


def fetch_pages() -> List:
    if not os.path.isfile(dbname):
        print(
            f"Cannot find {dbname} database. Run `make all` to create it and populate it with data."
        )
        sys.exit()

    try:
        con = sqlite3.connect(dbname)
        cur = con.cursor()

        one_day_ago = datetime.now() - timedelta(days=1)
        query = (
            "SELECT title, url, summary, categories FROM pages WHERE created_at >= ?;"
        )
        cur.execute(query, (one_day_ago,))
        results = cur.fetchall()
        return results
    except sqlite3.Error as err:
        print(f"Error: {err}")
    finally:
        if con:
            con.close()
