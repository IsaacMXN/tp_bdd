from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

class ImdbInfo(BaseModel):
    rating: Optional[float] = None
    votes: Optional[int] = None
    id: Optional[int] = None

class Awards(BaseModel):
    wins: Optional[int] = None
    nominations: Optional[int] = None
    text: Optional[str] = None

class ViewerInfo(BaseModel):
    fresh: Optional[int] = None

class CriticInfo(BaseModel):
    rotten: Optional[int] = None

class TomatoesInfo(BaseModel):
    viewer: Optional[ViewerInfo] = None
    critic: Optional[CriticInfo] = None
    lastUpdated: Optional[datetime] = None

class Movie(BaseModel):
    id: str = Field(alias="_id")
    plot: Optional[str] = None
    genres: Optional[List[str]] = None
    runtime: Optional[int] = None
    cast: Optional[List[str]] = None
    poster: Optional[str] = None
    title: str
    fullplot: Optional[str] = None
    languages: Optional[List[str]] = None
    released: Optional[datetime] = None
    directors: Optional[List[str]] = None
    rated: Optional[str] = None
    awards: Optional[Awards] = None
    lastupdated: Optional[str] = None
    year: Optional[int] = None
    imdb: Optional[ImdbInfo] = None
    countries: Optional[List[str]] = None
    type: Optional[str] = None
    tomatoes: Optional[TomatoesInfo] = None
    num_mflix_comments: Optional[int] = None

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "573a1390f29313caabcd42e8",
                "plot": "A group of bandits stage a brazen train hold-up...",
                "genres": ["Short", "Western"],
                "runtime": 11,
                "cast": ["A.C. Abadie", "Gilbert M. 'Broncho Billy' Anderson", "George Barnes", "Justus D. Barnes"],
                "poster": "https://m.media-amazon.com/images/M/MV5BMTU3NjE5NzYtYTYyNS00MDVmLWIwYj...",
                "title": "The Great Train Robbery",
                "fullplot": "Among the earliest existing films in American cinema...",
                "languages": ["English"],
                "released": "1903-12-01T00:00:00.000+00:00",
                "directors": ["Edwin S. Porter"],
                "rated": "TV-G",
                "awards": {"wins": 1, "nominations": 0, "text": "1 win."},
                "lastupdated": "2015-08-13 00:27:59.177000000",
                "year": 1903,
                "imdb": {"rating": 7.4, "votes": 9847, "id": 439},
                "countries": ["USA"],
                "type": "movie",
                "tomatoes": {
                    "viewer": {"fresh": 6},
                    "critic": {"rotten": 0},
                    "lastUpdated": "2015-08-08T19:16:10.000+00:00"
                },
                "num_mflix_comments": 0
            }
        }

class MovieUpdate(BaseModel):
    plot: Optional[str]
    genres: Optional[List[str]]
    runtime: Optional[int]
    cast: Optional[List[str]]
    poster: Optional[str]
    title: Optional[str]
    fullplot: Optional[str]
    languages: Optional[List[str]]
    released: Optional[datetime]
    directors: Optional[List[str]]
    rated: Optional[str]
    awards: Optional[Awards]
    lastupdated: Optional[str]
    year: Optional[int]
    imdb: Optional[ImdbInfo]
    countries: Optional[List[str]]
    type: Optional[str]
    tomatoes: Optional[TomatoesInfo]
    num_mflix_comments: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "plot": "A new plot description...",
                "genres": ["Drama"],
                "runtime": 120
            }
        }
