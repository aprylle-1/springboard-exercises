"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
default_img = "https://t3.ftcdn.net/jpg/03/46/83/96/360_F_346839683_6nAPzbhpSkIpb8pmAwufkC7c5eD7wYws.jpg"
def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User Model"""

    __tablename__ = "users"

    def __repr__(self):
        """Show information about User object"""
        u = self
        return f'first_name : {u.first_name} , last_name : {u.last_name}'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(50), nullable=False)

    last_name = db.Column(db.String(50), nullable=False)

    image_url = db.Column(db.String(200), nullable=True)

    @classmethod
    def add_user(cls, first_name, last_name, image_url=default_img):
        """Function that adds a user to the database"""
        new_user = cls(first_name=first_name, last_name=last_name, image_url=image_url)
        db.session.add(new_user)
        db.session.commit()

        return new_user.id

    @classmethod
    def get_all_users(cls):
        """Function that gets all the users from the database"""
        users = cls.query.all()
        return users

    @classmethod
    def get_user_by_id(cls, id):
        """Function that gets user details by user ID"""

        user = cls.query.get(id)
        return user
    
    @classmethod
    def delete_user(cls, id):
        """Function that deletes user"""

        user = cls.query.get(id)
        db.session.delete(user)
        db.session.commit()

    def get_user_full_name(self):
        """Returns user's full name as a single string"""
        
        return f"{self.first_name} {self.last_name}"

