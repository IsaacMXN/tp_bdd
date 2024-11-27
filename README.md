
## Requirements

- Python 3.8+
- MongoDB (or MongoDB Atlas for cloud)
- Neo4j (either local or cloud instance)

## Setup

### 1. Clone the repository

```bash
git clone https://your-repository-url.git
cd your-repository-name
```

### 2. Create and activate a virtual environment

#### On Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

#### On Windows:

```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install dependencies

Make sure you have `pip` updated, then install the required dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

This will install the following packages:

- `fastapi` – Web framework for building APIs.
- `python-dotenv` – For loading environment variables from `.env` files.
- `pymongo` – MongoDB driver.
- `neo4j` – Neo4j Python driver.
- `pydantic` – Data validation and settings management.
- `bson` – For handling MongoDB-specific types like `ObjectId`.
- `uvicorn` – ASGI server for running FastAPI applications.

### 4. Set up environment variables

Create a `.env` file in the root of the project and set the following variables:

```env
# MongoDB
MONGODB_URL=mongodb+srv://<username>:<password>@cluster0.pf4v4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
MONGODB_NAME=sample_mflix

# Neo4j
BOLT_URI=<neo4j-address>
USERNAME=<neo4j-username>
PASSWORD=<neo4j-password>
```

### 5. Run the application

Once everything is set up, you can run the application using `uvicorn`:

```bash
uvicorn main:app --reload
```

This will start the FastAPI application on `http://127.0.0.1:8000`.

---

## API Endpoints

### 1. **List All Movies**

- **Endpoint:** `/movies/`
- **Method:** `GET`
- **Description:** Get a list of all movies in the MongoDB database.
- **Response:**
  - Returns a list of movie objects with details like title, genres, cast, etc.

### 2. **Search Movies by Name or Actor**

- **Endpoint:** `/movies/search`
- **Method:** `GET`
- **Query Parameters:**
  - `movie_name`: (Optional) Search for movies by title.
  - `actor_name`: (Optional) Search for movies by actor.
- **Response:**
  - Returns a list of movies that match the search criteria.

### 3. **Update Movie by Title**

- **Endpoint:** `/movies/{title}`
- **Method:** `PUT`
- **Description:** Update a movie's information by its title.
- **Body:** A JSON object with the fields you want to update (e.g., plot, cast, genres, etc.)
- **Response:**
  - Returns the updated movie object.

### 4. **Get Number of Common Movies between MongoDB and Neo4j**

- **Endpoint:** `/movies/common_movies`
- **Method:** `GET`
- **Description:** Get the number of common movies between MongoDB and Neo4j.
- **Response:**
  - Returns the count of movies that exist in both databases.

### 5. **Get List of Users Who Rated a Specific Movie**

- **Endpoint:** `/movies/movie_ratings`
- **Method:** `GET`
- **Query Parameters:**
  - `movie_title`: The title of the movie to get ratings for.
- **Response:**
  - Returns a list of users who rated the movie along with their ratings and summary.

### 6. **Get List of Movies Rated by a Specific User**

- **Endpoint:** `/movies/user_movie_ratings`
- **Method:** `GET`
- **Query Parameters:**
  - `user_name`: The name of the user to get rated movies for.
- **Response:**
  - Returns a user object containing the number of movies rated and the list of movie titles rated.

---

## Project Structure

- **`main.py`**: FastAPI application and database connections (MongoDB, Neo4j).
- **`models.py`**: Pydantic models for movie and update validation.
- **`routes.py`**: API routes for movie listings, search, updates, and ratings.
- **`.env`**: Environment file containing MongoDB and Neo4j credentials.

---

