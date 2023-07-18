# Import necessary modules and libraries
from flask import Flask, request, jsonify
import requests

# Create a Flask web application
app = Flask(__name__)

# Define a constant variable for a valid API key
VALID_API_KEY = "260cdb2f0b9569143a580580c4deb0b6"

# Define the base URL for the movie API
MOVIE_API_BASE_URL = "https://api.tmdb.org/3/"

# Function to validate the API key provided by the user
def validate_api_key(api_key):
    """
    Validate the provided API key against the valid API key.

    Parameters:
        api_key (str): The API key to be validated.

    Returns:
        bool: True if the API key is valid, False otherwise.
    """
    return api_key == VALID_API_KEY

# Before every request is processed, this function is executed to check the validity of the API key.
@app.before_request
def authenticate_request():
    """
    Authenticate the request by checking the API key validity.
    If the API key is missing or invalid, it returns a 401 Unauthorized response.
    """
    api_key = request.args.get("api_key")
    if not api_key or not validate_api_key(api_key):
        return jsonify({"error": "Invalid API key"}), 401

# Route to fetch details of a specific movie by its name.
@app.route("/movies/<string:movie_name>", methods=["GET"])
def get_movie_details(movie_name):
    """
    Fetch details of a specific movie by its name.

    Parameters:
        movie_name (str): The name of the movie.

    Returns:
        JSON: The details of the first matching movie as a JSON response.
              If the movie is not found, it returns a 404 Not Found response with an error message.
    """
    api_key = request.args.get("api_key")
    response = requests.get(f"{MOVIE_API_BASE_URL}search/movie", params={"api_key": api_key, "query": movie_name})
    data = response.json()
    if "results" in data and len(data["results"]) > 0:
        movie = data["results"][0]
        return jsonify(movie)
    return jsonify({"error": "Movie not found"}), 404

# Route to fetch a list of all available movies.
@app.route("/movies", methods=["GET"])
def get_all_movies():
    """
    Fetch a list of all available movies.

    Returns:
        JSON: The list of available movies as a JSON response.
              If no movies are found, it returns a 404 Not Found response with an error message.
    """
    api_key = request.args.get("api_key")
    response = requests.get(f"{MOVIE_API_BASE_URL}discover/movie", params={"api_key": api_key})
    data = response.json()
    if "results" in data:
        return jsonify(data["results"])
    return jsonify({"error": "No movies found"}), 404

# Start the Flask app in debug mode if this script is run directly.
if __name__ == "__main__":
    app.run(debug=True)
