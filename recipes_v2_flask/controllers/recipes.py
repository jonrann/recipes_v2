# import app, user module, recipe module, flask
from recipes_v2_flask import app
from recipes_v2_flask.models import user as user_module
from recipes_v2_flask.models import recipe as recipe_module
from flask import render_template, redirect, url_for, request, session, flash
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash

# Route for viewing single recipe - render_template, GET
@app.route('/recipes/<int:recipe_id>')
def view_recipe(recipe_id):
    # Get data from recipe by retrieving id using class method
    if 'user_id' in session:
        user =  user_module.User.get_by_id(session['user_id'])
        recipe = recipe_module.Recipe.get_by_id(recipe_id)
        print(recipe.creator)
        return render_template('view_recipe.html', user=user, recipe=recipe)
    else:
        flash('Please log in', 'danger')
        return redirect(url_for('login_register'))
        # return rendering template


# Route for creating recipe page - render_template
@app.route('/recipes/new')
def create_recipe():
    if 'user_id' not in session:
        return redirect(url_for('register_login'))
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
@app.route('/recipes/edit/<int:recipe_id>')
def edit_recipe(recipe_id):
    user_id = session['user_id']
    user = user_module.User.get_by_id(user_id)
    recipe = recipe_module.Recipe.get_by_id(recipe_id)
    return render_template('edit_recipe.html', user=user, recipe=recipe)

# Route for editing recipe - POST, GET
@app.route('/recipes-edit', methods=['POST'])
def edit():
    recipe_data = dict(request.form)
    recipe_id = recipe_data['id']
    if recipe_module.Recipe.update_recipe(recipe_data) == None: #Because the query returns None
        flash('Recipe updated!', 'success')
    else: #if the query returns something other than None (eg. an error message)
        flash('Error updating', 'danger')
        return redirect(url_for('edit_recipe', recipe_id=recipe_id))
    updated_recipe = recipe_module.Recipe.get_by_id(recipe_id)

    return redirect(url_for('edit_recipe', recipe_id=updated_recipe.id))

# Route for deleting a recipe - POST
@app.route('/recipes/delete/<int:recipe_id>', methods=['POST'])
def delete(recipe_id):
    if 'user_id' in session:
        if recipe_module.Recipe.delete_recipe(recipe_id) == None:
            flash('Recipe deleted!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Failed deleting recipe', 'danger')
            return redirect(url_for('dashboard'))
    else:
        # if not in session redirect
        return redirect(url_for('register_login'))
