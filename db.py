from pymongo import MongoClient
from bson import ObjectId
import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']
client = MongoClient("mongodb+srv://<db_username>:<db_password>@cluster0.xzr3hrx.mongodb.net/") # chnage db user name & password
db = client["Movie_DB"]
class User:
    @classmethod
    def create(self,name, email, password):
        user = {
            "name": name,
            "email": email,
            "password": password
        }
        return db.users.insert_one(user)
    @classmethod
    def doesUserExist(self,email):
        if db.users.find_one({"email": email}): return True
        return False

class Genre:
    @classmethod
    def create(self,name):
        existing_genre = db.genres.find_one({"name": name})
        isCreated = True
        if existing_genre:
            isCreated = False
            return str(existing_genre['_id']),isCreated
        
        genre = {
            "name": name
        }
        result = db.genres.insert_one(genre)
        genre_id = str(result.inserted_id)

        return genre_id,isCreated
    @classmethod
    def findGenre(self,name):
        existing_genre = db.genres.find_one({"name": name})
        if existing_genre:
            return str(existing_genre['_id'])
        return False
class Movie:
    @classmethod
    def create(self,name, description, genre, release_date):
        movie_id = Movie.findMovie(name)
        if(movie_id):
            return str(movie_id),-1
        genre_id = Genre.findGenre(genre)
        if(not genre_id):
            return False,0
        movie = {
            "name": name,
            "description": description,
            "genre_id": ObjectId(genre_id),
            "release_date": release_date
        }
        result = db.movies.insert_one(movie)
        return str(result.inserted_id),1
    @classmethod
    def findMovie(self,name):
        movie_id = db.movies.find_one({"name": name})
        if(movie_id):
            return str(movie_id["_id"])
        return False
    @classmethod
    def update(self,movie_id, updates):
        return db.movies.update_one({"_id": ObjectId(movie_id)}, {"$set": updates})
    @classmethod
    def listMovies(self,filters):
        movies = db.movies.find(filters)
        movie_list = []
        for movie in movies:
            movie_list.append({
                "name": movie["name"],
                "description": movie["description"],
                "genre": db.genres.find_one({"_id": ObjectId(str(movie['genre_id']))})['name'],
                "release_date": movie["release_date"]
            })
        return movie_list
class Review:
    def create(self, movie_id, user_id, comment, rating):
        review = {
            "movie_id": ObjectId(movie_id),
            "user_id": ObjectId(user_id),
            "comment": comment,
            "rating": rating
        }
        return db.reviews.insert_one(review)

    def get_reviews_by_movie(self, movie_id):
        return db.reviews.find({"movie_id": ObjectId(movie_id)})

    def get_reviews_by_user(self, user_id):
        return db.reviews.find({"user_id": ObjectId(user_id)})
