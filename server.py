from recipes_v2_flask import app
# Import controllers when made.
from recipes_v2_flask.controllers import users
from recipes_v2_flask.controllers import recipes


if __name__ == "__main__":
    app.run(debug=True)