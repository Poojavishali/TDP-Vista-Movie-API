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
    return api_key == VALID_API_KEY

# Before every request is processed, this function is executed to check the validity of the API key.
@app.before_request
def authenticate_request():
    # Extract the API key from the query parameters of the request.
    api_key = request.args.get("api_key")
    
    # If the API key is missing or invalid, return a JSON response with an error message and 401 status code.
    if not api_key or not validate_api_key(api_key):
        return jsonify({"error": "Invalid API key"}), 401

# Route to fetch details of a specific movie by its name.
@app.route("/movies/<string:movie_name>", methods=["GET"])
def get_movie_details(movie_name):
    # Extract the API key from the query parameters of the request.
    api_key = request.args.get("api_key")
    
    # Send a request to the external movie API to search for the movie by name.
    response = requests.get(f"{MOVIE_API_BASE_URL}search/movie", params={"api_key": api_key, "query": movie_name})
    data = response.json()
    
    # If the search result contains movie data, return the details of the first movie as a JSON response.
    if "results" in data and len(data["results"]) > 0:
        movie = data["results"][0]
        return jsonify(movie)

    # If the movie is not found, return a JSON response with an error message and 404 status code.
    return jsonify({"error": "Movie not found"}), 404

# Route to fetch a list of all available movies.
@app.route("/movies", methods=["GET"])
def get_all_movies():
    # Extract the API key from the query parameters of the request.
    api_key = request.args.get("api_key")
    
    # Send a request to the external movie API to discover all movies.
    response = requests.get(f"{MOVIE_API_BASE_URL}discover/movie", params={"api_key": api_key})
    data = response.json()
    
    # If the API response contains a list of movies, return it as a JSON response.
    if "results" in data:
        return jsonify(data["results"])

    # If no movies are found, return a JSON response with an error message and 404 status code.
    return jsonify({"error": "No movies found"}), 404

# Start the Flask app in debug mode if this script is run directly.
if __name__ == "__main__":
    app.run(debug=True)
