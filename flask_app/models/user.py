from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:

    DB = 'recipes_schema'

    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_user(user):
        SpecialSym =['$', '@', '#', '%']
        is_valid = True 
        if len(user['first_name']) < 3:
            flash("First Name must be at least 3 characters.")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last Name must be at least 3 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        if len(user['password']) < 6:
            flash('length should be at least 6')
            is_valid = False
        if len(user['password']) > 20:
            flash('length should be not be greater than 8')
            is_valid = False
        if not user['password'] == user['confirm_password']:
            is_valid = False
        if not any(char.isdigit() for char in user['password']):
            flash('Password should have at least one numeral')
            is_valid = False
        if not any(char.isupper() for char in user['password']):
            flash('Password should have at least one uppercase letter')
            is_valid = False
            
        if not any(char.islower() for char in user['password']):
            flash('Password should have at least one lowercase letter')
            is_valid = False
            
        if not any(char in SpecialSym for char in user['password']):
            print('Password should have at least one of the symbols $@#')
            is_valid = False
        return is_valid
    

    # CREATE 
    @classmethod
    def save(cls, data):
        query = """
                INSERT INTO users (first_name, last_name, email, password)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
                """
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    

    # READ
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_one(cls, user_id):
        query = """SELECT * FROM users WHERE id = %(id)s"""
        data = {
            'id' : user_id
        }
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])