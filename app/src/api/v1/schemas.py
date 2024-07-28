from datetime import datetime

import orjson
from pydantic import BaseModel, Field
from typing import List, Optional

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
    score: int = Field(..., description="likes score")


class Review(BaseUserEventsModel):
    user_id: str = Field(..., description="user id")
    film_id: str = Field(..., description="film id")
    text: str = Field(..., description="review text")
    user_score: int = Field(..., description="user score")


class ReviewFromDB(Review):
    date_posted: datetime = Field(default_factory=datetime.now, description="when review was added")
    average_score: float = Field(0.0, description="average score")
    likes: List[Like] = Field(default_factory=list, description="list of likes")


class FilmScore(BaseUserEventsModel):
    film_id: str = Field(..., description="film id")
    score: int = Field(..., description="film score")
    created_at: datetime = Field(default_factory=datetime.now, description="when score was added")


class User(BaseUserEventsModel):
    scores: Optional[FilmScore] = Field(default_factory=list, description="list of film scores")
    bookmarks: Optional[list] = Field(default_factory=list, description="list of bookmarks")
