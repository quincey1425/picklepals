from flask_app.config.mysqlconnection import connectToMySQL
from flask import session, url_for, redirect, flash

class Pal:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.ranking = data['ranking']
        self.user = None

    @classmethod
    def get_friend_by_name(cls, friend_name):
        query = "SELECT * FROM pals WHERE CONCAT(first_name, ' ', last_name) = %(friend_name)s;"
        data = {'friend_name': friend_name}
        result = connectToMySQL('picklepals').query_db(query, data)
        if result:
            return cls(result[0])
        return None
    
    @staticmethod
    def is_friend(user_id, pal_id):
        query = "SELECT * FROM pals WHERE user_id = %(user_id)s AND id = %(pal_id)s;"
        data = {'user_id': user_id, 'pal_id': pal_id}
        result = connectToMySQL('picklepals').query_db(query, data)
        return bool(result)
    
    @classmethod
    def save(cls, data):
        user_id = session.get('user_id')
        data['user_id'] = user_id
        friend_name = f"{data['first_name']} {data['last_name']}"
        existing_friend = cls.get_friend_by_name(friend_name, user_id)

        if existing_friend:
            return False  # Friend already exists
        else:
            query = "INSERT INTO pals (first_name, last_name, ranking, user_id) VALUES (%(first_name)s, %(last_name)s, %(ranking)s, %(user_id)s);"
            try:
                connectToMySQL('picklepals').query_db(query, data)
                return True  # Friend added successfully
            except:
                return False  # Failed to add friend

    @classmethod
    def get_friend_by_name(cls, friend_name, user_id):
        query = "SELECT * FROM pals WHERE CONCAT(first_name, ' ', last_name) = %(friend_name)s AND user_id = %(user_id)s;"
        data = {'friend_name': friend_name, 'user_id': user_id}
        result = connectToMySQL('picklepals').query_db(query, data)
        if result:
            return cls(result[0])
        return None
    

    @classmethod
    def get_friends_by_user(cls, user_id):
        query = "SELECT * FROM pals WHERE user_id = %(user_id)s;"
        data = {'user_id': user_id}
        results = connectToMySQL('picklepals').query_db(query, data)
        friends = [cls(result) for result in results]
        return friends
    
    @classmethod
    def delete_friend(cls, user_id, friend_id):
        query = "DELETE FROM pals WHERE user_id = %(user_id)s AND id = %(friend_id)s;"
        data = {'user_id': user_id, 'friend_id': friend_id}
        try:
            connectToMySQL('picklepals').query_db(query, data)
            return True
        except:
            return False
