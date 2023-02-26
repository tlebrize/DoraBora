import os
import psycopg
from psycopg.rows import dict_row


class BaseDatabase:
    def __init__(self, name=None):
        name = name or os.getenv("DB_NAME")
        self.connection = psycopg.connect(
            f"postgresql://postgres:password@localhost:5432/{name}",
            autocommit=True,
            row_factory=dict_row,
        )

    def execute(self, *args, **kwargs):
        data = []
        with self.connection.cursor() as cursor:
            cursor.execute(*args, **kwargs)
            try:
                for row in cursor:
                    data.append(row)
            except psycopg.ProgrammingError:
                pass

        self.connection.commit()
        return data

    def get(self, id_):
        return self.model(
            **self.execute(
                f"SELECT * FROM {self.table} WHERE id = %(id)s;",
                {"id": id_},
            )[0]
        )

    def get_by(self, key, value):
        return self.model(
            **self.execute(
                f"select * from {self.table} WHERE {key} = %(value)s;",
                {"value": value},
            )[0]
        )

    def list(self):
        return self.list_model(
            [
                self.model(**row)
                for row in self.execute(
                    f"SELECT * FROM {self.table};",
                )
            ]
        )

    def create(self, values):
        keys = list(sorted(values.keys()))
        fields = ", ".join(keys)
        parameters = ", ".join([f"%({field})s" for field in keys])
        return self.model(
            **self.execute(
                f"""
INSERT INTO {self.table} ( {fields} )
VALUES ( {parameters} ) RETURNING *;""",
                dict(sorted(values.items())),
            )[0]
        )

    def set(self, id_, key, value):
        self.execute(
            f"UPDATE {self.table} SET {key} = %(value)s WHERE id = %(id)s;",
            {"id": id_, "value": value},
        )
