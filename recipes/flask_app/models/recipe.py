
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session, request
from flask_app.models import user

# The above is used when we do login registration, flask-bcrypt should already be in your env check the pipfile

# Remember 'fat models, skinny controllers' more logic should go in here rather than in your controller. Your controller should be able to just call a function from the model for what it needs, ideally.

class Recipe:
    db = "recipes" #which database are you using for this project
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.under = data['under']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.confirm_password = None
        self.creator = None
        # What changes need to be made above for this project?
        #What needs to be added here for class association? !!!!!!!!!!!!!



    # Create Recipe Models
    @classmethod
    def create_new_recipe(cls,recipe_data):
        if not cls.validate_recipe(recipe_data): return False
        query = """
            INSERT INTO 
            recipes 
            (name, under, description, instructions, date_made, user_id)
            VALUES (%(name)s, %(under)s, %(description)s, %(instructions)s, %(date_made)s, %(user_id)s);"""
        return connectToMySQL(cls.db).query_db(query,recipe_data)


    # Read Recipe Models
    @classmethod
    def get_recipe_by_id(cls,id):
        data = {'id': id}
        query = """
            SELECT *
            FROM recipes
            WHERE id = %(data)s;"""
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        if results:
            return cls(results[0])
        return False


    @classmethod
    def get_all_recipes_with_creator(cls):
        query = """
            SELECT *
            FROM recipes
            LEFT JOIN users
            ON users.id = recipes.user_id;"""
        results = connectToMySQL(cls.db).query_db(query)
        all_recipes = []
        for result in results:
            this_recipe = cls(result)
            this_recipe.creator = user.User.instantiate_user(result)
            all_recipes.append(this_recipe)
        return all_recipes
    
    
    @classmethod
    def get_one_recipe_with_creator(cls,data):
        id = {'id': data}
        query = """
            SELECT *
            FROM recipes
            LEFT JOIN users
            ON users.id = recipes.user_id
            WHERE recipes.id = %(id)s;"""
        results = connectToMySQL(cls.db).query_db(query,id)
        print("this is the result", results)
        for result in results:
            this_recipe = cls(result)
            this_recipe.creator = user.User.instantiate_user(results[0])
        return this_recipe

    # Update Recipe Models

    @classmethod
    def update_one_recipe(cls,data, recipe_id):
        if not cls.validate_recipe(data): return False
        data = {'id' : recipe_id,
            'name': data['name'],
            'under': data['under'],
            'description': data['description'],
            'instructions': data['instructions'],
            'date_made': data['date_made']}
        query = """
            UPDATE recipes
            SET name = %(name)s, under = %(under)s, description = %(description)s, instructions = %(instructions)s ,date_made = %(date_made)s
            WHERE id = %(id)s;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        print(query)
        print(results)
        return 
        

    # Delete Recipe Models
    
    @classmethod
    def delete_user_recipe(cls,recipe_id):
        data = {'id' : recipe_id}
        query = """
            DELETE FROM recipes
            where id = %(id)s;"""
        return connectToMySQL(cls.db).query_db(query, data)
    
    # validate Recipe
    
    @classmethod
    def validate_recipe(cls, data):
        is_valid = True
        if len(data['name']) < 3:
            flash("Name is required.")
            is_valid = False
        if len(data['description']) < 3:
            flash("Description is required.")
            is_valid = False
        if len(data['instructions']) < 3:
            flash("Instructions is required.")
            is_valid = False
        if not data['date_made']:
            flash("A date is requited.")
            is_valid = False
        return is_valid
