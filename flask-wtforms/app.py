from timeit import default_timer
from flask import Flask, request, redirect, render_template, session
from models import db, Pet, connect_db
from flask_debugtoolbar import DebugToolbarExtension
from forms import PetForm

app = Flask(__name__)
#app configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt_pets'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret_key_used_so_that_session_works"

connect_db(app)

@app.route("/")
def list_all_pets():
    """List all pets"""
    
    pets = Pet.query.all()
    return render_template("homepage.html", pets=pets)

@app.route("/add", methods=["GET", "POST"])
def add_pet_form():
    """GETS or PROCESSES Pet Form"""

    form = PetForm()
    default_image = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/1024px-No_image_available.svg.png"
    
    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.age.data
        available = form.available.data

        if photo_url:
            pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes, available=available)
            db.session.add(pet)
            db.session.commit()

        else:
            pet = Pet(name=name, species=species, photo_url=default_image, age=age, notes=notes, available=available)
            db.session.add(pet)
            db.session.commit()

        return redirect("/")
    
    else:
        return render_template("add_pet_form.html", form=form)

@app.route("/<pet_id>", methods=["POST", "GET"])
def edit_pet_form(pet_id):
    """Get pet details and displays them in a page"""

    pet = Pet.query.get(pet_id)
    form = PetForm(obj=pet)
    default_image = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/1024px-No_image_available.svg.png"

    if form.validate_on_submit():
        pet.name = form.name.data
        pet.species = form.species.data
        pet.age = form.age.data
        pet.notes = form.age.data
        pet.available = form.available.data
        
        if not form.photo_url.data:
            pet.photo_url = default_image
        else:
            pet.photo_url = form.photo_url.data
        db.session.commit()

        return redirect("/")
    else:
        return render_template("pet_details.html",pet=pet, form=form)