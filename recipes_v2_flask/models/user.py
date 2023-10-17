from recipes_v2_flask.config.mysqlconnection import connectToMySQL
from recipes_v2_flask.models import recipe as recipe_module
from flask import request, flash
import re

# create email regular expression
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# create User class
class User:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []

# create CR functions (no delete or update for users for this specifc project)
# Create
    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO users (
                first_name,
                last_name,
                email,
                password,
                created_at,
                updated_at
            )
            VALUES (
                %(first_name)s,
                %(last_name)s,
                %(email)s,
                %(password)s,
                NOW(),
                NOW()
            );
        """
        return connectToMySQL('recipes_v2_schema').query_db(query, data)

# Read All
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('recipes_v2_schema').query_db(query)
        users = []
        for row in results:
            if row:
                users.append(cls(row)) # intialziing each result (row) as an object in the users list
            else:
                return None
        return users

    # Read one
    @classmethod
    def get_by_id(cls, user_id):
        # Write the query to get one single user by its id
        query = "SELECT * FROM users WHERE id = %(id)s;"
        data = {
            'id' : user_id
        }
        # Run the query in MySQL to get back a result
        result = connectToMySQL('recipes_v2_schema').query_db(query, data)
        # Intialize the first result I get (which should only be one result) into an object using __init__ function.
        if result:
            return cls(result[0])
        else:
            return None
        # Return the object

    @classmethod
    def get_by_email(cls, email):
        # Write query that gets user by email (one email should belong to one id)
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data = {
            'email' : email
        }
        # Run query and get result from db
        result = connectToMySQL('recipes_v2_schema').query_db(query, data)
        # Intialize first result (only one)
        if result:
            return cls(result[0])
        else:
            return None
        # Return user data

    # Get recipes FROM users
    @classmethod
    def get_recipes_with_users(cls):
        query = """
            SELECT recipes.*, users.id AS user_id, users.first_name, users.last_name, users.email, users.password, users.created_at, users.updated_at
            FROM recipes
            JOIN users ON recipes.user_id = users.id
            ORDER BY recipes.updated_at DESC;
        """
        results = connectToMySQL('recipes_v2_schema').query_db(query)
        recipes_with_users_list = []
        if results:
            users = {}
            for row in results:
                # Create or reuse a user object
                user_id = row['user_id']
                if user_id not in users:
                    user_data = {
                        'id': user_id,
                        'first_name': row['first_name'],
                        'last_name': row['last_name'],
                        'email': row['email'],
                        'password': row['password'],
                        'created_at': row['created_at'],
                        'updated_at': row['updated_at']
                    }
                    users[user_id] = cls(user_data)

                # Create recipe object
                recipe_data = {
                    'id': row['id'],
                    'name': row['name'],
                    'description': row['description'],
                    'instructions': row['instructions'],
                    'under': row['under'],
                    'created_at': row['created_at'],
                    'updated_at': row['updated_at']
                }
                recipe = recipe_module.Recipe(recipe_data)
                recipe.creator = users[user_id]
                recipes_with_users_list.append(recipe)
            return recipes_with_users_list
        else:
            return None


    # Validator for Registration form
    @staticmethod
    def validate_user(data):
        is_valid = True

        # Validate first name
        if len(data['first_name']) < 3:
            flash('First name needs to be at least 3 characters', 'danger')
            is_valid = False

        # Validate last name
        if len(data['last_name']) < 3:
            flash('Last name needs to be at least 3 characters', 'danger')
            is_valid = False

        # Validate email
        if not EMAIL_REGEX.match(data['email']):
            flash('Invalid email', 'danger')
            is_valid = False

        # Validate password
        if len(data['password']) < 5:
            flash('Password needs to be at least 3 characters', 'danger')
            is_valid = False
        if not re.search("[A-Z]", data['password']):
            flash('Password needs at least 1 capital letter', 'danger')
            is_valid = False
        if not re.search("[0-9]", data['password']):
            flash('Password needs at least 1 number', 'danger')
            is_valid = False

        # Validate confirme password
        if data['password'] != data['confirm_password']:
            flash('Passwords do not match', 'danger')
            is_valid = False
        return is_valid
