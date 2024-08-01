from datetime import datetime

from pydantic import BaseModel, Field


class Pagination(BaseModel):
    per_page: int
    page: int


class Like(BaseModel):
    user_id: str = Field(..., description="user id")
    score: int


class LikeSchemaIn(BaseModel):
    film_id: str
    score: int


class LikeDeleteSchema(BaseModel):
    film_id: str


class ReviewIn(BaseModel):
    film_id: str = Field(..., description="film id")
    text: str
    user_score: int


class Review(BaseModel):
    user_id: str = Field(..., description="user id")
    film_id: str = Field(..., description="film id")
    text: str
    user_score: int


class ReviewFromDB(Review):
    date_posted: datetime = Field(default_factory=datetime.now)
    average_score: float = 0.0
    likes: list[Like] = []


class FilmScore(BaseModel):
    film_id: str
    score: int
    created_at: datetime = Field(default_factory=datetime.now)


class User(BaseModel):
    scores: list[FilmScore] = []
    bookmarks: list[str] = []


class BookmarksForUser(BaseModel):
    bookmarks: list[str] = []


class Film(BaseModel):
    _id: str
    average_score: float
    scores: list[Like]
