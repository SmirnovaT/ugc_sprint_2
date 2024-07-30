from uuid import UUID

from pymongo import MongoClient
from pymongo.collection import Collection

from generator_events.events import generate_new_bookmark, generate_new_like
from generator_events.generate_to_db import generate_events
from generator_events.test_utils.utils import time_it

TOTAL = 100
BATCH_SIZE = 100


def mongo_conn():
    client = MongoClient("localhost", 27017)
    db = client["test_db"]
    users_collection = db["users"]
    return db, users_collection


@time_it(TOTAL=TOTAL)
def insert_many_documents(users_collection, event_generator) -> None:
    """Множественная вставка закладок пользователей"""

    for batch in event_generator:
        db_data = []
        for data in batch:
            reform_data = {
                "_id": data["user_id"],
                "timestamp": data["timestamp"],
                "fingerprint": data["fingerprint"],
                "bookmarks": [data["film_id"]],
            }
            db_data.append(reform_data)
        users_collection.insert_many(db_data)


def insert_document(*, collection: Collection, data: dict) -> None:
    collection.insert_one(data)


@time_it(TOTAL=TOTAL)
def get_events(users_collection):
    """Получение пачки записей"""

    documents = users_collection.find().limit(TOTAL)
    return documents


def get_by_id(id_: UUID, field: str, users_collection) -> dict | list:
    """Получение записи по id"""

    data = users_collection.find_one({"_id": id_})
    if data:
        return data.get(field, [])
    else:
        return []


@time_it(TOTAL=1)
def get_bookmarks_for_user(users_collection) -> list[str]:
    """Получение списка закладок пользователя"""

    bookmark_data = generate_new_bookmark()

    film_id = bookmark_data["film_id"]
    user_id = bookmark_data["user_id"]

    db_data = {
        "_id": user_id,
        "timestamp": bookmark_data["timestamp"],
        "fingerprint": bookmark_data["fingerprint"],
        "bookmarks": [film_id],
    }

    insert_document(collection=users_collection, data=db_data)

    bookmarks = get_by_id(user_id, "bookmarks", users_collection)

    return bookmarks


@time_it(TOTAL=1)
def get_likes_for_user(users_collection: dict) -> list[dict]:
    """Получение списка лайков пользователя"""

    like_data = generate_new_like()

    user_id = like_data["user_id"]

    db_data = {
        "_id": user_id,
        "timestamp": like_data["timestamp"],
        "fingerprint": like_data["fingerprint"],
        "scores": [
            {
                "film_id": like_data["film_id"],
                "score": like_data["score"],
                "created_at": like_data["created_at"],
            }
        ],
    }

    insert_document(collection=users_collection, data=db_data)

    likes = get_by_id(user_id, "scores", users_collection)

    return likes


if __name__ == "__main__":
    db, users_collection = mongo_conn()

    event_generator = generate_events(count=TOTAL, batch_size=BATCH_SIZE)

    insert_many_documents(users_collection, event_generator)

    get_events(users_collection)

    get_bookmarks_for_user(users_collection)

    get_likes_for_user(users_collection)

    users_collection.delete_many({})
