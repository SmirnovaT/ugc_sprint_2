import random
import uuid

from datetime import timezone, timedelta, datetime

import faker

fake = faker.Faker()


def generate_event(event_type, data_dict) -> dict:
    """Базовая функция для генерации событий"""

    return {
        "event": {
            "type": event_type,
            "timestamp": fake.date_time_this_year(
                before_now=True, after_now=False, tzinfo=timezone(timedelta(hours=3))
            ).isoformat(),
            "user_id": str(uuid.uuid4()),
            "fingerprint": f"{fake.user_agent()} {fake.random_int(min=1000, max=9999)}x{fake.random_int(min=1000, max=9999)} UTC+3; {fake.locale()} Windows; {str(uuid.uuid4())}",
            "data": data_dict,
        }
    }

# ---- Likes ----
def generate_new_like() -> dict:
    """Добавление нового лайка для фильма """

    return generate_event(
        "new like",
        {
            "film_id": str(uuid.uuid4()),
            "user_id": str(uuid.uuid4()),
            "score": fake.random_int(min=0, max=10)
        },
    )

def generate_new_like_for_review() -> dict:
    """Добавление нового лайка для реыью """

    return generate_event(
        "new like for review",
        {
            "film_id": str(uuid.uuid4()),
            "review_id": str(uuid.uuid4()),
            "user_id": str(uuid.uuid4()),
            "score": fake.random_int(min=0, max=10)
        },
    )
# --- Reviews -----
def generate_new_review() -> dict:
    """Добавление нового обзора"""

    return generate_event(
        "new review",
        {
            "film_id": str(uuid.uuid4()),
            "user_id": str(uuid.uuid4()),
            "text": str,
            "date_posted": datetime
        },
    )

# --- Bookmark -----
def generate_new_bookmark()-> dict:
    """Добавление новой закладки"""

    return generate_event(
        "new bookmark",
        {
            "user_id": str(uuid.uuid4()),
            "film_id": str(uuid.uuid4())
        },
    )

