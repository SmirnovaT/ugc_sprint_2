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
    user_id: str = Field(..., description="user id")
    score: int


class Like_with_film_id(Like):
    film_id: str


class ReviewIn(BaseUserEventsModel):
    film_id: str = Field(..., description="film id")
    text: str
    user_score: int


class Review(BaseUserEventsModel):
    user_id: str = Field(..., description="user id")
    film_id: str = Field(..., description="film id")
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
    bookmarks: list[str] = []


class BookmarksForUser(BaseUserEventsModel):
    bookmarks: list[str] = []


class Film(BaseModel):
    _id: str
    average_score: float
    scores: list[Like]
