import random
import uuid

from datetime import timezone, timedelta
from typing import Generator

import faker

fake = faker.Faker()


def generate_to_db() -> dict:
    """Функция генерирует данные для тестирования БД"""

    return {
        "type": "click",
        "timestamp": fake.date_time_this_year(
            before_now=True, after_now=False, tzinfo=timezone(timedelta(hours=3))
        ).isoformat(),
        "user_id": str(uuid.uuid4()),
        "fingerprint": f"{fake.user_agent()} {fake.random_int(min=1000, max=9999)}x{fake.random_int(min=1000, max=9999)} UTC+3; {fake.locale()} Windows; {str(uuid.uuid4())}",
        "element": random.choice(["film", "video", "article", "image"]),
        "url": f'http://{random.choice(["example", "google", "youtube"])}.com',
    }


def generate_events(count: int, batch_size: int) -> Generator[list[dict], None, None]:
    """Генерирует 10млн записей и возвращает пачками по 500 записей"""

    def event_generator() -> Generator[list[dict], None, None]:
        batch = []
        for i in range(count):
            batch.append(generate_to_db())
            if len(batch) == batch_size:
                yield batch
                batch = []
        if batch:
            yield batch

    return event_generator()