import uuid

from datetime import datetime, timedelta, timezone

import faker

fake = faker.Faker()


def generate_event() -> dict:
    """Базовая функция для генерации событий"""

    return {
        "timestamp": fake.date_time_this_year(
            before_now=True, after_now=False, tzinfo=timezone(timedelta(hours=3))
        ).isoformat(),
        "fingerprint": f"{fake.user_agent()} {fake.random_int(min=1000, max=9999)}x{fake.random_int(min=1000, max=9999)} UTC+3; {fake.locale()} Windows; {str(uuid.uuid4())}",

    }


# ---- Likes ----
def generate_new_like() -> dict:
    """Добавление нового лайка для фильма """

    event_data = generate_event()
    event_data.update({
        "film_id": str(uuid.uuid4()),
        "user_id": str(uuid.uuid4()),
        "score": fake.random_int(min=0, max=10),
        "created_at": fake.date_time_this_year(
            before_now=True, after_now=False, tzinfo=timezone(timedelta(hours=3))
        ).isoformat(),
    })
    return event_data


def generate_new_like_for_review() -> dict:
    """Добавление нового лайка для ревью """

    event_data = generate_event()
    event_data.update({
        "film_id": str(uuid.uuid4()),
        "review_id": str(uuid.uuid4()),
        "user_id": str(uuid.uuid4()),
        "score": fake.random_int(min=0, max=10)
    })
    return event_data


# --- Reviews -----
def generate_new_review() -> dict:
    """Добавление нового обзора"""
    event_data = generate_event()
    event_data.update({
        "film_id": str(uuid.uuid4()),
        "user_id": str(uuid.uuid4()),
        "text": fake.text(),
        "date_posted": datetime.now()
    })
    return event_data


# --- Bookmark -----
def generate_new_bookmark() -> dict:
    """Добавление новой закладки"""

    event_data = generate_event()
    event_data.update({
        "user_id": str(uuid.uuid4()),
        "film_id": str(uuid.uuid4())
    })
    return event_data
