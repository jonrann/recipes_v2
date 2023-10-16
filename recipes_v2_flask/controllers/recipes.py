# import app, user module, recipe module, flask
from recipes_v2_flask import app
from recipes_v2_flask.models import user as user_module
from recipes_v2_flask.models import recipe as recipe_module
from flask import render_template, redirect, url_for, request, session, flash
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash

# Route for viewing single recipe - render_template, GET

# Route for creating recipe page - render_template

# Route for creating a recipe - POST

# Route for editing recipe page - render_template

# Route for editing recipe - POST, GET

# Route for deleting a recipe - POST

