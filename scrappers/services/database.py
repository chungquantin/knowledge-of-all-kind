#!/usr/bin/python

import psycopg2


def get_sql_command(command: str):
    return open(f"src/commands/{command}.sql", "r").read()


class DatabaseService:
    __connection = None

    @classmethod
    def connect(cls):
        if not cls.__connection:
            print('Establishing connection...')
            cls.__connection = psycopg2.connect(
                database="postgres", user='admin', password='secret', host='127.0.0.1', port='5432'
            )
            if cls.__connection:
                print("Connection established: ", cls.__connection)

        return cls.__connection
