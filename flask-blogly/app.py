"""Blogly application."""

from crypt import methods
from email.mime import image
from flask import Flask, render_template, request, redirect, session
from models import db, connect_db, User, default_img

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "fasdfsdhjfhjsdgfhsdfhkwe"


connect_db(app)

@app.route('/')
def home_page():
    """View will list all users in database - Will be fixed in the future"""
    
    users = User.get_all_users()
    
    return render_template('home.html', users=users)

@app.route('/users')
def list_all_users():
    """List All Users"""

    users = User.get_all_users()

    return render_template('users.html', users=users)

@app.route('/users/new', methods=['GET'])
def show_create_user_form():
    """Directs user to Create User Form"""
    errors = session.get("errors", [])
    if errors:
        session["errors"] = []
    return render_template('create-user-form.html', errors=errors)

@app.route('/users/new', methods=['POST'])
def create_user():
    """Create New User from Form Submission"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    errors = []
    if not first_name:
        errors.append("Please indicate your first name.")
    if first_name and len(first_name) > 50:
        errors.append("First Name must be 50 characters only")
    if not last_name:
        errors.append("Please indicate your last name")
    if last_name and len(last_name) > 50:
        errors.append("Last Name must be 50 characters only")

    if len(errors) > 0:
        session["errors"] = errors
        return redirect("/users/new")

    if image_url:
        user_id = User.add_user(first_name=first_name, last_name=last_name, image_url=image_url)
    else:
        user_id = User. add_user(first_name=first_name, last_name=last_name)

    return redirect("/users")

@app.route('/users/<user_id>', methods=['GET'])
def show_user_details(user_id):
    """Show User Details"""

    user = User.get_user_by_id(user_id)
    
    return render_template('user-details.html', user=user)

@app.route('/users/<user_id>/edit', methods=['GET'])
def show_edit_form(user_id):
    """Generate Edit User Form"""

    user = User.get_user_by_id(user_id)

    return render_template('edit-user.html', user=user)

@app.route('/users/<user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """Commit Edited Details of User"""

    user = User.get_user_by_id(user_id)
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    if image_url:
        user.image_url = image_url
    else:
        user.image_url = default_img
    user.first_name = first_name
    user.last_name = last_name

    db.session.commit()

    return redirect("/users")

@app.route('/users/<user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete User by ID"""

    User.delete_user(user_id)
    return redirect("/users")