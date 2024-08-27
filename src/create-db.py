import os
import sqlite3
import sys

dbname = "llm-reader.db"

if os.path.isfile(dbname):
    print(f"{dbname} already exists. Exiting")
    sys.exit()

con = sqlite3.connect(f"{dbname}")
cur = con.cursor()
cur.execute("""
CREATE TABLE pages
    (id			INTEGER PRIMARY KEY AUTOINCREMENT,
    title		TEXT,
    url			TEXT,
    summary		TEXT,
    user		TEXT,
    categories	TEXT,
    created_at	timestamp);
""")
con.close()

print(f"Database {dbname} created successfully")
