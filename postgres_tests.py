import json
from contextlib import contextmanager
import logging

import psycopg2

from generator_events.generate_to_db import generate_events
from generator_events.test_utils.utils import time_it

TOTAL =10000000
BATCH_SIZE = 100000

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
        values = [
            (event['type'],
             event['timestamp'],
             event['user_id'],
             event['fingerprint'],
             event['element'],
             event['url'])
            for event in batch
        ]

        insert_events(values)

def insert_events(values):
    client.execute("""INSERT INTO event (type, timestamp, user_id, fingerprint, element, url)
            VALUES """, values)

if __name__ == "__main__":
    event_generator = generate_events(count=TOTAL, batch_size=BATCH_SIZE)

    with conn_context(dsn=dsn) as conn_pg:
        cursor = conn_pg.cursor()
        logging.warning("Creating a database")
        cursor.execute('CREATE DATABASE IF NOT EXISTS example')
        cursor.execute("""DROP TABLE IF EXISTS users""")
        logging.warning("Creating a table")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id UInt32,
            info jsonb);""")
        logging.warning("generating events")
    event_generator = generate_events(count=TOTAL, batch_size=BATCH_SIZE)
    transform_data(event_generator, insert_events)
    get_events(limit=TOTAL)
    update_events(limit=TOTAL)
    drop_events()