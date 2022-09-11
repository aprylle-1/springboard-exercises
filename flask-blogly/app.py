"""Blogly application."""

from crypt import methods
from email.mime import image
from flask import Flask, render_template, request, redirect, session
from models import db, connect_db, User, Post, default_img, PostTag, Tag
from sqlalchemy import desc
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "fasdfsdhjfhjsdgfhsdfhkwe"


connect_db(app)

@app.route('/')
def home_page():
    """Gets 5 Most Recent Post"""
    
    top_five_latest_posts = Post.query.order_by(desc(Post.created_at)).limit(5).all()

    return render_template('home.html', posts=top_five_latest_posts)

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
    
    errors = session.get("errors", [])
    session["errors"] = []

    user = User.get_user_by_id(user_id)
    posts = user.posts
    return render_template('user-details.html', user=user, posts=posts, errors=errors)

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
    user = User.query.get(user_id)
    posts = user.posts
    errors = []
    if posts:
        errors.append("Cannot delete user with posts")
        session["errors"] = errors
        return redirect(f"/users/{user_id}")
    
    else:
        User.delete_user(user_id)
    return redirect("/users")

@app.route("/users/<user_id>/posts/new", methods=["GET"])
def get_add_post_form(user_id):
    """Route that directs the user to the creat post form"""
    
    errors = []
    
    if session.get("errors", []):
        errors = session["errors"]
        session["errors"] = []
    
    user = User.query.get(user_id)
    tags = Tag.query.all()
    
    return render_template('create-post-form.html', user = user, errors=errors, tags=tags)

@app.route("/users/<user_id>/posts/new", methods=["POST"])
def add_post_for_user(user_id):
    """Route that processes the post request"""
    
    errors = []
    title = request.form["title"]
    content = request.form["content"]

    tags = request.form.getlist("tags")

    if not title:
        errors.append("Missing title")
    if not content:
        errors.append("Content Missing")
    
    if errors:
        session["errors"] = errors
        return redirect(f"/users/{user_id}/posts/new")

    post = Post(title=title, content=content, user_id=user_id, created_at=datetime.now())
    db.session.add(post)
    db.session.commit()

    post_tags = [PostTag(post_id=post.id, tag_id=tag) for tag in tags]
    db.session.add_all(post_tags)
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

    tags = Tag.query.all()

    post_tag_ids = [tag.tag_id for tag in post.tags]

    return render_template('edit-post.html', post=post, errors = errors, tags=tags, post_tag_ids=post_tag_ids)

@app.route("/posts/<post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """Route that processes the edit post request"""
    errors = []
    title = request.form["title"]
    content = request.form["content"]
    tags = request.form.getlist("tags")
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

        for post_tag in post.tags:
            db.session.delete(post_tag)

        db.session.commit()
    
        for tag in tags:
            new_tag = PostTag(post_id=post_id, tag_id=tag)
            db.session.add(new_tag)
        db.session.commit()
    
        return redirect(f"/posts/{post_id}")

@app.route("/posts/<post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get(post_id)
    
    post_tags = post.tags

    for post_tag in post_tags:
        db.session.delete(post_tag)
        db.session.commit()
    
    user_id = post.user.id
    
    db.session.delete(post)
    
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route("/tags")
def get_all_tags():
    tags = Tag.query.all()

    return render_template("tags.html", tags=tags)

@app.route("/tags/<tag_id>")
def show_tag_details(tag_id):
    tag = Tag.query.get(tag_id)
    posts_tags = tag.posts

    posts = []

    for post in posts_tags:
        posts.append(post.post)

    return render_template("tag-details.html", tag=tag, posts=posts)

@app.route("/tags/new", methods=["GET"])
def get_add_tag_form():

    errors = session.get("errors", [])
    session["errors"] = []

    return render_template("create-tag-form.html", errors = errors)

@app.route("/tags/new", methods=["POST"])
def add_tag():

    name = request.form.get("name", "")
    all_tags = Tag.query.all()
    names = []
    for tag in all_tags:
        names.append(tag.name)

    errors = []
    if not name:
        errors.append("No tag name was submitted")
        session["errors"] = errors
        return redirect("/tags/new")

    elif name and name in names:
        errors.append("Tag name already exists")
        session["errors"] = errors
        return redirect("/tags/new")
    
    else:
        tag = Tag(name=name)
        db.session.add(tag)
        db.session.commit()
        return redirect("/tags")

@app.route("/tags/<tag_id>/edit", methods=["GET"])
def get_edit_tag_form(tag_id):

    errors = session.get("errors", [])
    tag = Tag.query.get(tag_id)
    session["errors"] = []
    return render_template("edit-tag.html", errors=errors, tag=tag)

@app.route("/tags/<tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):

    tag = Tag.query.get(tag_id)
    name = request.form.get("name", "")
    errors = []
    all_tags = Tag.query.all()
    names = [tag.name for tag in all_tags]
    
    if not name:
        errors.append("Tag Name is a required field")
        session["errors"] = errors
        return redirect(f"/tags/{tag_id}/edit")
    if name == tag.name:
        return redirect("/tags")
    if name and name in names:
        session["errors"] = errors
        errors.append("Tag Name already exists")
        return redirect(f"/tags/{tag_id}/edit")
    
    tag.name = name
    db.session.commit()
    return redirect("/tags")

@app.route("/tags/<tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):

    tag = Tag.query.get(tag_id)
    posts = tag.posts

    if posts:
        for post in posts:
            db.session.delete(post)
    
    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")
