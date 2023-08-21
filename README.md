# Shipmnts_Dev


Certainly! Here's a README file template that you can use to explain your code's functionality, endpoints, and response formats:

---

# IMDb Backend API Clone

This project implements a Flask-based backend API for an IMDb-like movie database. The API allows users to create users, add genres, create movies, update movies, list movies, add reviews to movies, and fetch reviews for movies. The API is built using Flask and MongoDB for data storage.

## Setup

1. Install the required Python packages by running:
   ```
   pip install Flask pymongo
   ```

2. Replace `"YOUR_MONGODB_URI"` and `"your_database_name"` in the code with your actual MongoDB Atlas URI and database name.

3. Run the Flask app:
   ```
   python app.py
   ```

## Endpoints

### Create User

- **Route:** `/users`
- **Method:** POST
- **Description:** Create a user with the provided name, email, and password.
- **Request Body:**
  ```json
  {
    "name": "User Name",
    "email": "user@example.com",
    "password": "user_password"
  }
  ```
- **Response:** JSON object with a status message and response details.

### Create Genre

- **Route:** `/genres`
- **Method:** POST
- **Description:** Add a new movie genre.
- **Request Body:**
  ```json
  {
    "name": "Action"
  }
  ```
- **Response:** JSON object with a status message, genre_id, and response details.

### Create Movie

- **Route:** `/movies`
- **Method:** POST
- **Description:** Add a new movie with details.
- **Request Body:**
  ```json
  {
    "name": "Movie Name",
    "description": "Movie description",
    "genre": "Action",
    "release_date": "YYYY-MM-DD"
  }
  ```
- **Response:** JSON object with a status message, movie_id, and response details.

### Update Movie

- **Route:** `/movies/<movie_id>`
- **Method:** PUT
- **Description:** Update a movie's description, genre, or release date.
- **Request Body:** Include fields to update (description, genre, release_date).
- **Response:** JSON object with a status message and response details.

### List Movies

- **Route:** `/movies/list_movies/`
- **Method:** GET
- **Description:** List movies based on filters (name, genre, release_date).
- **Query Parameters:** `name`, `genre`, `release_date`
- **Response:** JSON object with a list of movies and response details.

### Add Review

- **Route:** `/movies/<movie_id>/reviews`
- **Method:** POST
- **Description:** Add a review for a specific movie.
- **Request Body:**
  ```json
  {
    "comment": "Great movie!",
    "rating": 5,
    "email": "user@example.com"
  }
  ```
- **Response:** JSON object with a status message, review_id, and response details.

### Fetch Reviews

- **Route:** `/movies/<movie_id>/reviews`
- **Method:** GET
- **Description:** Fetch reviews for a specific movie.
- **Response:** JSON object with a list of reviews and response details.

## Response Format

For successful requests, the API responds with status codes in the `200` range and returns a JSON object with a `status` field indicating success (`"OK"`) or failure (`"Fail"`), a `message` field with a descriptive message, and additional response-specific fields.

For example:
```json
{
  "message": "User created successfully",
  "status": "OK",
  "response": 1
}
```
