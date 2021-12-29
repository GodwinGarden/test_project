from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import artist


class Painting:
    db_name = 'artists_paintings'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.title = db_data['title']
        self.description = db_data['description']
        self.price = db_data['price']
        self.artist = None
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.artist_id = db_data['artist_id']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO paintings (title, description, price, artist_id) VALUES (%(title)s,%(description)s,%(price)s,%(artist_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM paintings;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_paintings = []
        for row in results:
            print(row['painting_title'])
            all_paintings.append(cls(row))
        return all_paintings

    @classmethod
    def get_all_with_artists(cls):
        query = "SELECT * FROM paintings JOIN artists ON artists.id = artist_id;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_paintings = []
        for row in results:
            this_painting = cls(row)
            artist_dict = {
                'id':row['artists.id'],
                'first_name':row['first_name'],
                'last_name':row['last_name'],
                'email':row['email'],
                'password':row['password'],
                'created_at':row['artists.created_at'],
                'updated_at':row['artists.updated_at']
            }
            this_artist = artist.Artist(artist_dict)
            this_painting.artist = this_artist
            all_paintings.append(this_painting)
        return all_paintings
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM paintings JOIN artists on artists.id = artist_id WHERE paintings.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        this_painting=cls(results[0])
        # need to create a dictionary {} for each get_one
        artist_dict = {
            'id':results[0]['artists.id'],
            'first_name':results[0]['first_name'],
            'last_name':results[0]['last_name'],
            'email':results[0]['email'],
            'password':results[0]['password'],
            'created_at':results[0]['artists.created_at'],
            'updated_at':results[0]['artists.updated_at']
        }      
        this_artist=artist.Artist(artist_dict)
        this_painting.artist=this_artist 
        return this_painting


    @classmethod
    def update(cls, data):
        query = "UPDATE paintings SET title=%(title)s, description=%(description)s, price=%(price)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM paintings WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_painting(painting):
        is_valid = True
        if len(painting['title']) < 3:
            is_valid = False
            flash("Title must be at least 3 characters","painting")
        if len(painting['description']) < 3:
            is_valid = False
            flash("Description must be at least 3 characters","painting")
        if int(painting['price']) < 1:
            is_valid = False
            flash("Please enter a positive price","painting")
        return is_valid