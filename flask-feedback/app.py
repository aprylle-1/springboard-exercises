from flask import Flask, redirect, render_template, request, flash, session
from models import User, connect_db, db, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config['SECRET_KEY'] = "secret_key_used_so_that_session_works"

connect_db(app)

@app.route("/")
def home_page():
    """Redirects user to register route"""
    
    return redirect("/register")

@app.route("/register", methods=["GET", "POST"])
def register_user():
    """Registers new user and saves details to database"""

    form = RegisterForm()

    if "user" in session:
        username = session["user"]
        return redirect(f"/users/{username}")

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Successfully Registered!", "success")
            session["user"] = new_user.username
            
            return redirect(f"/users/{new_user.username}")

        except:
            flash("Username already taken", "danger")
            return render_template("register.html", form=form)

    return render_template("register.html", form=form)

@app.route("/login", methods=["POST", "GET"])
def login_user():
    """Login user"""

    if "user" in session:
        username = session["user"]
        return redirect(f"/users/{username}")

    form = LoginForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        if User.login_user(username, password):
            user = User.login_user(username, password)
            session["user"] = user.username
            return redirect(f"/users/{user.username}")
        else:
            flash("Incorrect Username/Password.", "danger")
    
    return render_template("login.html", form=form)

@app.route("/logout", methods=["POST"])
def logout_user():
    """Logouts user, removes session storage - redirects to login"""

    session.pop("user")
    
    flash("Goodbye!", "primary")
    
    return redirect("/login")

@app.route("/users/<username>")
def show_user_details(username):
    """Logged in user's profile"""

    if "user" in session and username == session.get("user"):
        user = User.query.get(username)

        feedbacks = db.session.query(Feedback).join(User).filter(Feedback.username == username).order_by(Feedback.id.asc()).all()
        
        return render_template("user.html", user=user, feedbacks=feedbacks)
    
    else:
        flash("Please login", "danger")
        return redirect("/login")

@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """Delete only login user"""

    if "user" not in session:
        flash("You must login to delete your account", "danger")
        return redirect("/")

    if "user" in session and username != session.get("user"):
        flash("Access denied. Profile not yours", "danger")
        return redirect(f"/users/{username}")

    if username == session.get("user"):
        user = User.query.get(username)
        feedbacks = db.session.query(Feedback).join(User).filter(Feedback.username == username).all()
        for feedback in feedbacks:
            db.session.delete(feedback)
            db.session.commit()

        db.session.delete(user)
        db.session.commit()

        session.pop("user")

        return redirect("/")

@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):

    form = FeedbackForm()

    if not session.get("user"):
        flash("Please login", "info")
        return redirect("/login")

    if session.get("user") == username and form.validate_on_submit():
        
        title = form.title.data
        content = form.content.data
        
        feedback = Feedback(title=title, content=content, username=username)

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{username}")

    if session.get("user") != username:
        flash("Access denied")
        return redirect("f/users/{username}")
    
    else:
        return render_template("/add_feedback.html", form=form, username=username)

@app.route("/feedbacks/<feedback_id>/update", methods=["POST", "GET"])
def edit_feedback(feedback_id):

    feedback = Feedback.query.get(feedback_id)

    form = FeedbackForm(obj=feedback)

    if "user" not in session:
        flash("Please login", "info")
        return redirect("/login")

    elif session["user"] != feedback.username:
        flash("You are not authorized to edit this.", "danger")
        return redirect(f"/login")

    elif form.validate_on_submit():
        
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()
        
        return redirect(f"/users/{feedback.username}")

    return render_template("/edit_feedback.html", form=form, username=feedback.username)

@app.route("/feedbacks/<feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):

    feedback = Feedback.query.get(feedback_id)
    
    if not session.get("user"):
        flash("Please login", "danger")
        return redirect("/login")

    elif session["user"] != feedback.username:
        flash("You are not authorized to delete this")
        return redirect("/login")

    else:
        db.session.delete(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")



