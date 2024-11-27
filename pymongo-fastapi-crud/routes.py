from bson import ObjectId
from fastapi import APIRouter, Request, Query, Body, HTTPException, status
from typing import List, Optional

from models import Movie, MovieUpdate

router = APIRouter()

def convert_objectid_to_str(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, dict):
        return {key: convert_objectid_to_str(value) for key, value in obj.items()}
    if isinstance(obj, list):
        return [convert_objectid_to_str(item) for item in obj]
    return obj

@router.get("/", response_description="List all movies", response_model=List[Movie])
def list_movies(request: Request):
    movies = list(request.app.database["movies"].find(limit=100))
    movies = convert_objectid_to_str(movies)
    return movies


@router.get("/search", response_description="Get a movie by name or actor", response_model=List[Movie])
async def search_movies(
        request: Request,
        movie_name: Optional[str] = Query(None, title="Movie Name", max_length=100),
        actor_name: Optional[str] = Query(None, title="Actor Name", max_length=100)
):
    query = {}

    if movie_name:
        query["title"] = {"$regex": movie_name, "$options": "i"}

    if actor_name:
        query["cast"] = {"$regex": actor_name, "$options": "i"}

    movies_cursor = request.app.database["movies"].find(query)
    movies_list = list(movies_cursor)

    movies_list = convert_objectid_to_str(movies_list)

    return movies_list


@router.put("/{title}", response_description="Update a movie by title", response_model=Movie)
def update_movie(title: str, request: Request, movie: MovieUpdate = Body(...)):
    update_data = {k: v for k, v in movie.dict().items() if v is not None}

    if len(update_data) >= 1:
        update_result = request.app.database["movies"].update_one(
            {"title": title}, {"$set": update_data}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with title {title} not found")

    updated_movie = request.app.database["movies"].find_one({"title": title})
    if updated_movie is not None:
        return convert_objectid_to_str(updated_movie)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with title {title} not found")

@router.get("/common_movies", response_description="Number of common movies between MongoDB and Neo4j")
def get_common_movies(request: Request):
    # Step 1: Fetch movies from MongoDB
    mongodb_movies_cursor = request.app.database["movies"].find({}, {"title": 1, "_id": 0})
    mongodb_titles = {movie["title"] for movie in mongodb_movies_cursor}

    # Step 2: Fetch movies from Neo4j
    query = "MATCH (m:Movie) RETURN m.title AS title"
    neo4j_titles = set()
    with request.app.neo4j_driver.session() as session:
        result = session.run(query)
        neo4j_titles = {record["title"] for record in result}

    # Step 3: Find common titles
    common_titles = mongodb_titles & neo4j_titles  # Intersection of sets

    # Step 4: Return count of common movies
    return {"common_movies_count": len(common_titles)}


@router.get("/movie_ratings", response_description="List users who rated a specific movie")
def get_movie_ratings(movie_title: str, request: Request):
    """
    List users who rated a given movie.
    """
    query = """
    MATCH (p:Person)-[r:REVIEWED]->(m:Movie {title: $movie_title})
    RETURN p.name AS person, r.rating AS rating, r.summary AS summary
    """

    with request.app.neo4j_driver.session() as session:
        result = session.run(query, movie_title=movie_title)
        ratings = [{"person": record["person"], "rating": record["rating"], "summary": record["summary"]} for record in result]

    if not ratings:
        return {"message": f"No ratings found for movie: {movie_title}"}

    return {"movie": movie_title, "ratings": ratings}

@router.get("/user_movie_ratings", response_description="Get user and the list of movies they rated")
def get_user_movie_ratings(user_name: str, request: Request):
    """
    Return the user with the number of movies they have rated and the list of rated movies.
    """
    query = """
    MATCH (p:Person {name: $user_name})-[:REVIEWED]->(m:Movie)
    RETURN p.name AS person, count(m) AS rated_movies_count, collect(m.title) AS rated_movies
    """

    with request.app.neo4j_driver.session() as session:
        result = session.run(query, user_name=user_name)
        user_data = [{"person": record["person"],
                      "rated_movies_count": record["rated_movies_count"],
                      "rated_movies": record["rated_movies"]} for record in result]

    if not user_data:
        return {"message": f"No ratings found for user: {user_name}"}

    return {"user": user_data[0]}

