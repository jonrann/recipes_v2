# import app, user module, recipe module, flask, bcrypt
from recipes_v2_flask import app
from recipes_v2_flask.models import user as user_module
from recipes_v2_flask.models import recipe as recipe_module
from flask import render_template, redirect, url_for, request, session, flash
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash

bcrypt = Bcrypt(app)

# Route for routing to dashboard - render_template
@app.route('/')
def register_login():
    return render_template('login.html')

# Route for registering user - POST
@app.route('/register', methods=['POST'])
def register():
    # Retrieve data from register form
    user_data = dict(request.form)

    # Validate data from form
    if not user_module.User.validate_user(user_data):
        return redirect(url_for('register_login'))

    # Generate hashed PW
    hashed_pw = generate_password_hash(user_data['password'])
    user_data['password'] = hashed_pw

    # Save data into the database using classmethod from user.py
    if user_module.User.create(user_data):
        return redirect(url_for('dashboard')) #Create dashboard


# Route for logging in - POST
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    # Check if user exists by fetching email and retrive all data
    user = user_module.User.get_by_email(email)
    # If email exists, check if password matches hashed password using check pw hash
    print(user)
    if user:
        if check_password_hash(user.password, password):
        # If password matches, create a session with the user's id
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            flash('Incorrect password', 'danger')
            return redirect(url_for('register_login'))
    else:
        flash('Email not found','danger')
        return redirect(url_for('register_login'))

# Redirect to dashboard
@app.route('/recipes')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
    else:
        return redirect(url_for('register_login'))
    current_user = user_module.User.get_by_id(user_id)
    users = user_module.User.get_all()
    recipes = user_module.User.get_recipes_with_users()
    return render_template('dashboard.html', users=users, recipes=recipes, current_user=current_user)


# Route for logging out - POST
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('register_login'))