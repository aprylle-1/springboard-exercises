"""Blogly application."""

from crypt import methods
from email.mime import image
from flask import Flask, render_template, request, redirect, session
from models import db, connect_db, User, Post, default_img

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
    posts = user.posts
    return render_template('user-details.html', user=user, posts=posts)

@app.route('/users/<user_id>/edit', methods=['GET'])
def show_edit_form(user_id):
    """Generate Edit User Form"""
    errors = []
    user = User.get_user_by_id(user_id)
    if session.get("errors") is not None:
        errors = session.get("errors", [])
    session['errors'] = []
    
    return render_template('edit-user.html', user=user, errors = errors)

@app.route('/users/<user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """Commit Edited Details of User"""

    user = User.get_user_by_id(user_id)
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    errors = []
    if not first_name:
        errors.append("You have not entered a new first name")
    if first_name and len(first_name) > 50:
        errors.append("First Name must be 50 characters only")
    if not last_name:
        errors.append("You have not entered a new last name")
    if last_name and len(last_name) > 50:
        errors.append("Last Name must be 50 characters only")

    if len(errors) > 0:
        session["errors"] = errors
        return redirect(f'/users/{user_id}/edit')

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

@app.route("/users/<user_id>/posts/new", methods=["GET"])
def get_add_post_form(user_id):
    """Route that directs the user to the creat post form"""
    user = User.query.get(user_id)
    return render_template('create-post-form.html', user = user)

@app.route("/users/<user_id>/posts/new", methods=["POST"])
def add_post_for_user(user_id):
    """Route that processes the post request"""
    
    title = request.form["title"]
    content = request.form["content"]

    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()
    return redirect(f"/users/{user_id}")

@app.route("/posts/<post_id>")
def show_post_details(post_id):
    """Route that shows Post Details"""
    
    #is post_id does not exist returns None -> no exception is raised
    post = Post.query.get(post_id)

    #handling an invalid post_id -- create custom 404 error page
    if post is None:
        return "This page does not exist - Custom 404 error page goes here"

    return render_template("post-details.html", post=post)

@app.route("/posts/<post_id>/edit", methods=["GET"])
def get_edit_post_form(post_id):
    """Route that shows Edit Post Form"""
    
    errors = session.get("errors", [])

    session["errors"] = []
    
    post = Post.query.get(post_id)

    return render_template('edit-post.html', post=post, errors = errors)

@app.route("/posts/<post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """Route that processes the edit post request"""
    errors = []
    title = request.form["title"]
    content = request.form["content"]

    if not title:
        errors.append("Missing Post Title")
    if not content:
        errors.append("Missing Post Content Details")

    if len(errors) > 0:
        session["errors"] = errors
        return redirect(f"/posts/{post_id}/edit")
    
    else:
        post = Post.query.get(post_id)
        post.title = title
        post.content = content
    
        db.session.commit()
    
        return redirect(f"/posts/{post_id}")


@app.route("/posts/<post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get(post_id)
    
    user_id = post.user.id
    
    db.session.delete(post)
    
    db.session.commit()

    return redirect(f"/users/{user_id}")
