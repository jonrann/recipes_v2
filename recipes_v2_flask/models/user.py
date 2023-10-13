from recipes_v2_flask.config.mysqlconnection import connectToMySQL

# create email regular expression

# create User class
class User:
    def __init__(self, data) -> None:
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
                updated_at,
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
    def get_by_id(cls, data):
        # Write the query to get one single user by its id
        query = "SELECT * FROM users WHERE id = %(id)s;"
        # Run the query in MySQL to get back a result
        result = connectToMySQL('recipes_v2_schema').query_db(query, data)
        # Intialize the first result I get (which should only be one result) into an object using __init__ function.
        if result:
            return cls(result[0])
        else:
            return None
        # Return the object

    @classmethod
    def get_by_email(cls, data):
        # Write query that gets user by email (one email should belong to one id)
        query = "SELECT * FROM users WHERE email = %(email)s;"
        # Run query and get result from db
        result = connectToMySQL('recipes_v2_schema').query_db(query, data)
        # Intialize first result (only one)
        if result:
            return cls(result[0])
        else:
            return None
        # Return user data

    # Get recipes FROM users

        # Fetch data of recipes from one user using a JOIN query

        # Create user object

        # Create recipe object

        # Associate the objects with one another using user.recipes attribute and recipe.creator attribute

    # Validator for Registration form
        # Validate first name

        # Validate last name

        # Validate email

        # Validate password

        # Validate confirme password
