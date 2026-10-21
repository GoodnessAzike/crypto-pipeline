import os 
from pathlib import Path

import psycopg   # a postgres driver, how python talks to the db

MIGRATIONS_DIR = Path("migrations")
db_url = os.environ.get("DATABASE_URL", "postgresql://postgres:pw@localhost:5433/crypto") #get the database url, it uses DATABASE_URL as default if there is one, otherwise use the full url

with psycopg.connect(db_url) as conn:  # connects to the db, calls it conn so the next line can use it
    conn.execute("CREATE TABLE IF NOT EXISTS schema_migrations (version TEXT PRIMARY KEY, applied_at TIMESTAMPTZ NOT NULL DEFAULT now())")
    applied = {row[0] for row in conn.execute("SELECT version FROM schema_migrations")}  #ask db for every migrations, one row at a time and collect and sve as a set
    conn.commit() # make it permenant and not a transaction

    for path in sorted(MIGRATIONS_DIR.glob("*.sql")):  #finds every file in migration folder whose name ends in sql and put them in name order
        if path.name in applied:        # is the file name from line 11
            print("already applied:", path.name)
            continue
        conn.execute(path.read_text())  # opens .sql and read everything as a text and send the SQL to the db to run
        conn.execute("INSERT INTO schema_migrations (version) VALUES (%s)", (path.name,))  #add row into the checklist, use %s as a placeholder. the , after the path.name makes a list of one item
        conn.commit()
        print("applied:", path.name)