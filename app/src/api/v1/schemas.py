from datetime import datetime

import orjson
from pydantic import BaseModel, Field
from typing import List

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


class Review(BaseUserEventsModel):
    user_id: str = Field(..., description="user id")
    film_id: str = Field(..., description="film id")
    text: str
    user_score: int


class ReviewFromDB(Review):
    date_posted: datetime = Field(default_factory=datetime.now, description="when review was added")
    average_score: float = Field(0.0, description="average score")
    likes: List[Like] = Field(default_factory=list, description="list of likes")
