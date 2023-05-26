from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
from flask import flash
# from flask_app.models import sighting

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.ranking = data['ranking']
        self.about_me = data['about_me']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.pals = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('picklepals').query_db(query)
        users = []
        for d in results:
            users.append( cls(d) )
        return users
    
    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO users (first_name, last_name, email, password) 
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"""
        result = connectToMySQL('picklepals').query_db(query, data)
        return result
    
    @classmethod
    def save_two(cls, data):
        query = """
            INSERT INTO users (ranking, about_me) 
            VALUES (%(ranking)s, %(about_me)s);"""
        result = connectToMySQL('picklepals').query_db(query, data)
        return result
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * from users WHERE id = %(id)s"
        results = connectToMySQL('picklepals').query_db(query, data)
        if results:
            return cls(results[0])
        return None
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('picklepals').query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * from users WHERE email = %(email)s"
        results = connectToMySQL('picklepals').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def update_user_data(cls, data):
        query = "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, ranking=%(ranking)s, about_me=%(about_me)s WHERE id = %(id)s;"
        return connectToMySQL('picklepals').query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL('picklepals').query_db(query, data)
    
    @staticmethod
    def validate_register(user):
        valid = True
        query = "SELECT * from users WHERE email = %(email)s"
        results = connectToMySQL('picklepals').query_db(query, user)
        if len(results) >= 1:
            flash("Email already taken", "register")
            valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email", "register")
            valid = False
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters", "register")
            valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters", "register")
            valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", "register")
            valid = False
        if user['password'] != user['confirm']:
            flash("Passwords do not match", "register")
        return valid
    
    @staticmethod
    def validate_user_data(data):
        valid = True

        if len(data['first_name']) < 2:
            flash('First name must be at least 2 characters', 'update')
            valid = False

        if len(data['last_name']) < 2:
            flash('Last name must be at least 2 characters', 'update')
            valid = False

        if not data['ranking']:
            flash('Ranking is required', 'update')
            return False

        ranking = int(data['ranking'])
        if ranking < 1 or ranking > 8:
            flash('Ranking must be between 1 and 8', 'update')
            return False

        if len(data['about_me']) == 0:
            flash('About me is required', 'update')
            valid = False

        return valid
