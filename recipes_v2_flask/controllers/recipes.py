# import app, user module, recipe module, flask
from recipes_v2_flask import app
from recipes_v2_flask.models import user as user_module
from recipes_v2_flask.models import recipe as recipe_module
from flask import render_template, redirect, url_for, request, session, flash
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash

# Route for viewing single recipe - render_template, GET

# Route for creating recipe page - render_template
@app.route('/recipes/new')
def create_recipe():
    return render_template('create_recipe.html')

# Route for creating a recipe - POST
@app.route('/create-recipe', methods=['POST'])
def create():
    # Get current session id
    user_id = session['user_id']
    # Get all data from form and put in mutable dictionary
    recipe_data =  dict(request.form)
    recipe_data['user_id'] = user_id
    # Use class method to save new recipe
    if recipe_module.Recipe.create(recipe_data):
        flash('Recipe successfully created.', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Failed to make recipe', 'danger')
        return redirect(url_for('create_recipe'))

# Route for editing recipe page - render_template

# Route for editing recipe - POST, GET

# Route for deleting a recipe - POST

