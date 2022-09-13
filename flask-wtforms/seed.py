from models import db, Pet, connect_db
from app import app

connect_db(app)

db.drop_all()
db.create_all()

bobbie = Pet(name="Bobbie", species="cat", age=1, photo_url="https://cdn.pixabay.com/photo/2017/02/20/18/03/cat-2083492__340.jpg", notes="Male, already neutered, likes to beg for food", available=False)

gary = Pet(name="Gary", species="cat", age=1, photo_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/1024px-No_image_available.svg.png", notes="Male, already neutered, likes to beg for food, will scratch you if you scratch him", available=True)

hitler = Pet(name="Hitler", species="cat", age=1, photo_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/1024px-No_image_available.svg.png", notes="Male, already neutered, can't jump high", available=True)

george=Pet(name="George", species="dog", age=3, photo_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/1024px-No_image_available.svg.png", notes="Male, likes to run around", available=True)

pets = [bobbie, gary, hitler, george]

db.session.add_all(pets)
db.session.commit()