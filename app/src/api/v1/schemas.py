from datetime import datetime

import orjson
from pydantic import BaseModel, Field

from src.utils.json import orjson_dumps


class Pagination(BaseModel):
    per_page: int
    page: int


class BaseUserEventsModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Like(BaseUserEventsModel):
    user_id: str
    score: int


class Review(BaseUserEventsModel):
    user_id: str
    film_id: str
    text: str
    user_score: int


class ReviewFromDB(Review):
    date_posted: datetime = Field(default_factory=datetime.now)
    average_score: float = 0.0
    likes: list[Like] = []


class FilmScore(BaseUserEventsModel):
    film_id: str
    score: int
    created_at: datetime = Field(default_factory=datetime.now)


class User(BaseUserEventsModel):
    scores: list[FilmScore] = []
    bookmarks: list = []


class BookmarksForUser(BaseUserEventsModel):
    bookmarks: list = []
