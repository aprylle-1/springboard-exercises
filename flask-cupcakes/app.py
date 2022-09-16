"""Flask app for Cupcakes"""

from flask import Flask, jsonify, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, Cupcake, db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cupcakes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "fsdfhkfkjdshkfsdhjkfsd"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route("/")
def home_page():
    return render_template("home.html")

@app.route("/api/cupcakes")
def get_all_cupcakes():
    """List All Cupcates in Database"""
    cupcakes = Cupcake.query.all()
    cupcakes_serialized = [cupcake.serialize() for cupcake in cupcakes]
    return jsonify(cupcakes=cupcakes_serialized)

@app.route("/api/cupcakes/<cupcake_id>")
def get_cupcake(cupcake_id):
    """Get cupcake based on ID"""
    cupcake = Cupcake.query.get(cupcake_id)
    cupcake_serialized = cupcake.serialize()
    return jsonify(cupcake=cupcake_serialized)

@app.route("/api/cupcakes", methods=["POST"])
def add_cupcake():
    """Add a cupcake to the database"""
    flavor = request.json.get("flavor")
    size = request.json.get("size")
    rating = request.json.get("rating")
    image = request.json.get("image")

    if not flavor or not size or not rating:
        resp = {
            "message" : "missing required parameter"
        }
        return (jsonify(message=resp), 400)

    if image:
        cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    else:
        cupcake = Cupcake(flavor=flavor, size=size, rating=rating)

    db.session.add(cupcake)
    db.session.commit()

    cupcake_serialized= cupcake.serialize()

    return (jsonify(cupcake=cupcake_serialized), 201)

@app.route("/api/cupcakes/<cupcake_id>", methods=["PATCH"])
def edit_cupcake(cupcake_id):
    """Edit a cupcake's details (based on ID)"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    flavor = request.json.get("flavor")
    size = request.json.get("size")
    rating = request.json.get("rating")
    image = request.json.get("image")

    if flavor:
        cupcake.flavor = flavor
    if size:
        cupcake.size = size
    if rating:
        cupcake.rating = rating
    if image:
        cupcake.image = image

    db.session.commit()

    return (jsonify(cupcake=cupcake.serialize()), 200)

@app.route("/api/cupcakes/<cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Delete cupcake (based on ID)"""
    
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()

    return (jsonify({"message" : "Deleted"}), 200)
    
