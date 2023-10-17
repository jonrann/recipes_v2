from recipes_v2_flask.config.mysqlconnection import connectToMySQL

# create Recipe class
class Recipe:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under = data['under']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None

# CRUD Functions
# Create
    @classmethod
    def create(cls, data):
        # Query to put data in db
        query = """
            INSERT INTO recipes (
                user_id,
                name,
                description,
                instructions,
                under,
                created_at,
                updated_at
            )
            VALUES (
                %(user_id)s,
                %(name)s,
                %(description)s,
                %(instructions)s,
                %(under)s,
                NOW(),
                NOW()
            );
        """
        # return execution of query
        return connectToMySQL('recipes_v2_schema').query_db(query, data)

# Read
    @classmethod
    def get_all(cls):
        # Write query to get all recipes
        query = "SELECT * FROM recipes;"
        results = connectToMySQL('recipes_v2_schema').query_db(query)
        # Create empty list to hold recipe objects
        recipes = []
        if results:         # Check to see if any exist
        # Loop through results and intialize each as an object
            for row in results:
                recipes.append(cls(row))
            return recipes
        else:
            return None

    # Read one by id
    # Method to fetch data of one recipe by ID
    @classmethod
    def get_by_id(cls, recipe_id):
        # query for fetching data
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        data = {
            'id' : recipe_id
        }
        result = connectToMySQL('recipes_v2_schema').query_db(query, data)
        # Create object from result (should only be one fetched from query)
        if result:
            return cls(result[0])
        else:
            return None
            # Return object


# Update
    # Update classmethod for updating a recipe
    @classmethod
    def update_recipe(cls, data):
        # query to update query
        query = """
            UPDATE recipes
            SET name = %(name)s,
                description = %(description)s,
                instructions = %(instructions)s,
                under = %(under)s,
                updated_at = NOW()
            WHERE id = %(id)s;
        """
        # return executing query
        return connectToMySQL('recipes_v2_schema').query_db(query, data)

# Delete
    # method for deleting a recipe
    @classmethod
    def delete_recipe(recipe_id):
        #  query to delete
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        data = {
            'id' : recipe_id
        }
        # return execution
        return connectToMySQL('recipes_v2_schema').query_db(query, data)


