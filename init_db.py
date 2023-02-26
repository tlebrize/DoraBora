import os
import sys
from pprint import pprint

from dora_bora.database.base import BaseDatabase


def drop_db(db, dbname):
    print("Dropping database", dbname)
    db.execute(  # Clear existing connections
        """SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = %s
              AND pid <> pg_backend_pid();""",
        [dbname],
    )

    db.execute(f"DROP DATABASE IF EXISTS {dbname};")
    print("Done.\n")


def create_db(admin_db, dbname):
    print("Creating database", dbname)
    admin_db.execute(f"CREATE DATABASE {dbname};")


def apply_migrations(dbname):
    db = BaseDatabase(dbname)
    for file in sorted(os.listdir("migrations")):
        print(f"migrating: {file[2:-4]}...")
        with open(f"migrations/{file}", "r") as fd:
            db.execute(fd.read())
        print("Done !\n")


def main(dbname):
    admin_db = BaseDatabase("postgres")
    drop_db(admin_db, dbname)
    create_db(admin_db, dbname)
    apply_migrations(dbname)


if __name__ == "__main__":
    dbname = sys.argv[1]
    main(dbname)
