from contextlib import contextmanager
import logging

import psycopg2

from generator_events.generate_to_db import generate_events
from generator_events.events import generate_new_bookmark, generate_new_like
from generator_events.test_utils.utils import time_it

TOTAL =100000
BATCH_SIZE = 1000

dsn = {
    'dbname': 'postgres_db',
    'user': 'postgres_user',
    'password': 'postgres_password',
    'host': '127.0.0.1',
    'port': 5430,
    'options': '-c search_path=content',
}

@contextmanager
def conn_context(dsn: dict):
    conn_pg = psycopg2.connect(**dsn)
    try:
        yield conn_pg
    finally:
        conn_pg.close()

@time_it(TOTAL=TOTAL)
def transform_data(event_generator, insert_events):
    """Преобразование данных и вставка в БД"""
    logging.warning("Transforming data")
    for batch in event_generator:
        print(batch[0])
        values = [{
            "_id": event['user_id'],
            "scores": [
                {
                    "film_id": event['film_id'],
                    "score": event['score'],
                    "created_at": event['created_at'],
                }]
        }
            for event in batch
        ]

        insert_events(values)


def insert_events(values):
    values = ", ".join([f"('{value['_id']}', '{str(value).replace('\'', '\"')}')" for value in values])
    cursor.execute(f"""INSERT INTO public.users (user_id, data)
            VALUES {values}""")

@time_it(TOTAL=TOTAL)
def get_bookmarks_for_user() -> list[str]:
    """Получение списка закладок пользователя"""
    bookmarks = []
    for _ in range(TOTAL):
        bookmark_data = generate_new_bookmark()

        film_id = bookmark_data["film_id"]
        user_id = bookmark_data["user_id"]

        values = {
            "_id": user_id,
            "bookmarks": [film_id],
        }

        values_to_insert = f"('{values['_id']}', '{str(values).replace('\'', '\"')}')"
        cursor.execute(f"""INSERT INTO public.users (user_id, data)
        VALUES {values_to_insert}""")

        bookmarks.append(get_by_id(user_id, "bookmarks"))

    return bookmarks

@time_it(TOTAL=TOTAL)
def get_likes_for_user() -> list[dict]:
    """Получение списка лайков пользователя"""
    likes = []
    for _ in range(TOTAL):

        like_data = generate_new_like()

        user_id = like_data["user_id"]

        values = {
            "_id": user_id,
            "timestamp": like_data["timestamp"],
            "fingerprint": like_data["fingerprint"],
            "scores": [
                {
                    "film_id": like_data["film_id"],
                    "score": like_data["score"],
                "   created_at": like_data["created_at"],
                }
            ],
        }

        values_to_insert = f"('{values['_id']}', '{str(values).replace('\'', '\"')}')"
        cursor.execute(f"""INSERT INTO public.users (user_id, data)
                    VALUES {values_to_insert}""")

        likes.append(get_by_id(user_id, "scores"))

    return likes


@time_it(TOTAL=TOTAL)
def get_events(limit):
    cursor.execute(f"""SELECT * FROM public.users LIMIT {limit}""")

def get_by_id(id, key):
    cursor.execute(f"""SELECT data ->> '{key}' FROM public.users WHERE user_id = '{id}'""")

if __name__ == "__main__":
    event_generator = generate_events(count=TOTAL, batch_size=BATCH_SIZE)

    with conn_context(dsn=dsn) as conn_pg:
        cursor = conn_pg.cursor()
        conn_pg.autocommit = True
        logging.warning("Creating a database")
        cursor.execute("""SELECT 'CREATE DATABASE postgres_db' WHERE NOT EXISTS 
        (SELECT FROM pg_database WHERE datname = 'postgres_db')""")
        cursor.execute("""DROP TABLE IF EXISTS public.users""")
        logging.warning("Creating a table")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS public.users (
            user_id varchar(100),
            data jsonb);""")
        logging.warning("generating events")
        event_generator = generate_events(count=TOTAL, batch_size=BATCH_SIZE)
        transform_data(event_generator, insert_events)
        get_events(limit=TOTAL)
        get_bookmarks_for_user()
        get_likes_for_user()

        cursor.execute("""DROP TABLE IF EXISTS public.users""")