from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

class Recipe:

    DB = 'recipes_schema'

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30 = data['under_30']
        self.date_cooked = data['date_cooked']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.owner = None

    # VALIDATION
    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            flash('name must be filled out')
            is_valid = False
        if len(recipe['description']) < 3:
            flash('description must be filled out')
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash('instructions must be filled out')
            is_valid = False
        return is_valid
    
    # CREATE
    @classmethod
    def create_recipe(cls, data):
        query = """
                INSERT INTO recipes (name, description, instructions, under_30, date_cooked, user_id)
                VALUES (%(name)s, %(description)s, %(instructions)s, %(under_30)s, %(date_cooked)s, %(user_id)s)
                """
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result
    
    # READ
    @classmethod
    def get_all(cls):
        query = """SELECT * FROM recipes 
                LEFT JOIN users ON recipes.user_id = users.id;"""
        results = connectToMySQL(cls.DB).query_db(query)
        if not results:
            return []
        recipes = []
        for recipe in results:
            this_recipe = cls(recipe)
            data = {
                'id': recipe['users.id'],
                'first_name': recipe['first_name'],
                "last_name": recipe ['last_name'],
                'email': recipe['email'],
                'password': recipe['password'],
                'created_at': recipe['users.created_at'],
                'updated_at': recipe['users.updated_at']
            }
            creator = User(data)
            this_recipe.owner = creator
            recipes.append(this_recipe)
        return recipes
    
    @classmethod
    def get_one_recipe(cls, recipe_id):
        query = """ SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s"""
        data = {
            'id': recipe_id
        }
        results = connectToMySQL(cls.DB).query_db(query, data)
        recipe_creator = cls(results[0])
        print(results[0])
        owner_data = { 
        "id": results[0]['users.id'],
        "first_name": results[0]['first_name'],
        "last_name": results[0]['last_name'],
        "email": results[0]['email'],
        "password": results[0]['password'],
        "created_at": results[0]['created_at'],
        "updated_at": results[0]['updated_at']
        }
        recipe_creator.owner = User(owner_data)
        return recipe_creator

    # UPDATE 
    @classmethod
    def update(cls, data):
        query = """
                UPDATE recipes  SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, under_30 = %(under_30)s,
                date_cooked = %(date_cooked)s, updated_at = NOW() WHERE id = %(id)s
                """
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    
    # DELETE
    @classmethod
    def delete(cls, recipe_id):
        query  = "DELETE FROM recipes WHERE id = %(id)s;"
        data = {"id": recipe_id}
        return connectToMySQL(cls.DB).query_db(query, data)