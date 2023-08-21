from flask import Flask, request, jsonify
from pymongo import MongoClient
from db import *
import hashlib
app = Flask(__name__)
client = MongoClient("YOUR_MONGODB_URI")
db = client["your_database_name"]

# Create User
@app.route('/users', methods=['POST'])
def create_user(request):
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email').lower()
        password = hashlib.sha512(data.get('password').encode()).hexdigest()  # Encode the password before hashing

        
        # Check if user already exists
        if User.doesUserExist(email=email):
            return jsonify({"message": "User already exists","status":"OK","response":0}), 200
        try:
            User.create(name=name, email=email, password=password)
            return jsonify({"message": "User created successfully","status":"OK","response":1}), 200
        except:
            return jsonify({"message": "Something went wrong","status":"Fail","response":0}), 500
    except Exception as e:
        return jsonify({"message": "Something went wrong","status":"Fail","response":0}), 500
    
# Create Genres
@app.route('/genres', methods=['POST'])
def create_genre():
    try:
        data = request.get_json()
        name = data.get('name').lower()
        
        if not name:
            return jsonify({"message": "Name is required","status":"Fail"}), 400
        try:
            genre_id,isCreated = Genre.create(name)
            if(isCreated):
                return jsonify({"message":"Genre created successfully.","status":"OK","genre_id":genre_id}),200
            else:
                return jsonify({"message":"Genre already exists.","status":"OK","genre_id":genre_id}),200
        except Exception as e:
            print(e)
            return jsonify({"message":"Something went wrong","status":"Fail"}), 201
    except Exception as e:
        print(e)
        return jsonify({"message":"Something went wrong","status":"Fail"}), 500
        
# Create Movies
@app.route('/movies', methods=['POST'])
def create_movie():
    try:
        data = request.get_json()
        name = data.get('name').lower()
        description = data.get('description')
        genre = data.get('genre').lower()
        release_date = data.get('release_date')
        
        if (name and description and genre and release_date):
            return jsonify({"message": "All fields are required","status":"Fail"}), 400
        try:
            movie_id,resp = Movie.create(name, description, genre, release_date)
            if(movie_id and resp==1):
                return jsonify({"message":"Movie created successfully.","status":"OK","movie_id":movie_id}),200
            elif(resp==0):
                return jsonify({"message":"Genre does not exists.","status":"OK"}),200
            elif(resp==-1):
                return jsonify({"message":"Movie already exists.","status":"OK","movie_id":movie_id}),200
            else:
                return jsonify({"message":"Something went wrong","status":"Fail"}),500
                
        except Exception as e:
            print(e)
            return jsonify({"message":"Something went wrong","status":"Fail"}), 201
    except Exception as e:
        return jsonify({"message":"Something went wrong","status":"Fail"}), 500
# Update Movies
@app.route('/movies/<movie_id>', methods=['PUT'])
def update_movie(movie_id):
    try:
        data = request.get_json()
        updates = {}

        if 'description' in data:
            updates['description'] = data['description']
        if 'genre' in data:
            genre_id = Genre.findGenre(data['genre'])
            if not genre_id:
                return jsonify({"messgae": "Genre not found","status":"OK","response":0}), 200
            updates['genre_id'] = ObjectId(genre_id)
        if 'release_date' in data:
            updates['release_date'] = data['release_date']

        if not updates:
            return jsonify({"message": "No updates provided","status":"OK","response":0}), 200
        result = Movie.update(movie_id, updates)

        if result.modified_count > 0:
            return jsonify({"message": "Movie updated successfully","status":"OK","response":1}), 200
        else:
            return jsonify({"message": "Movie not found","status":"OK","response":0}), 404
    except Exception as e:
        return jsonify({"message": str(e),"status":"Fail"}), 500
# List Movies
@app.route('/movies/list_movies/', methods=['GET'])
def list_movies():
    try:
        name_filter = request.args.get('name')
        genre_filter = request.args.get('genre')
        release_date_filter = request.args.get('release_date')
        
        filters = {}
        if name_filter:
            filters['name'] = {"$regex": name_filter.lower(), "$options": "i"}
        if genre_filter:
            genre_id = Genre.findGenre(genre_filter.lower())
            if not genre_id:
                return jsonify({"message": "Genre not found","status":"Fail"}), 404
            filters['genre_id'] = ObjectId(genre_id)
        if release_date_filter:
            filters['release_date'] = release_date_filter
        movie_list = Movie.listMovies(filters=filters)
        
        return jsonify({"movies": movie_list,"message":"Movies listed as per filters.","status":"OK"}),200
    except Exception as e:
        return jsonify({"message": str(e),"status":"Fail"}), 500

# Add Review
@app.route('/movies/<movie_id>/reviews', methods=['POST'])
def add_review(movie_id):
    # Implement review creation logic
    return jsonify({"message": "Review added successfully"})

# Fetch Reviews
@app.route('/movies/<movie_id>/reviews', methods=['GET'])
def fetch_reviews(movie_id):
    # Implement review fetching logic
    return jsonify({"message": "List of reviews"})

# BONUS - Delete Movie (only by the user who added it)
@app.route('/movies/<movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    # Implement movie deletion logic with user verification
    return jsonify({"message": "Movie deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)

