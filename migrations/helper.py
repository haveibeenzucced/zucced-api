"""Helper module for executing raw SQL."""
import pathlib

from sqlalchemy import orm


def execute(bind, filename: str):
    session = orm.Session(bind=bind)
    path_str = "migrations/versions/{filename}".format(filename=filename)
    file_path = pathlib.Path(path_str).absolute()
    with open(file_path) as sql_file:
        sql_to_execute = sql_file.read()
        session.execute(sql_to_execute)
        session.commit()
