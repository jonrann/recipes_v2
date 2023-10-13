from recipes_v2_flask.config.mysqlconnection import connectToMySQL

# create Recipe class
class Recipe:
    def __init__(self, data) -> None:
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under = data['under']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

# CRUD Functions
# Create
    @classmethod
    def create(cls, data):
        # Query to put data in db
        query = """
            INSERT INTO recipes (
                name,
                description,
                instructions,
                under,
                created_at,
                updated_at
            )
            VALUES (
                %(name)s,
                %(description)s,
                %(instructions)s,
                %(under)s,
                NOW(),
                NOW(),
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

        # Return list


# Update



# Delete

