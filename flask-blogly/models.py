"""Models for Blogly."""

from datetime import datetime
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

    image_url = db.Column(db.String(200), nullable=False, default=default_img)

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

class Post(db.Model):
    """Post Model"""

    __tablename__ = "posts"

    datetime_now = datetime.now()

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(50), nullable=False)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime_now)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", backref="posts")

    def __repr__(self):
        """Show information about the Post Object"""
        p = self
        return f"<{p.title} {p.content}>"

    @classmethod
    def add_new_post(cls, title, content, user_id):
        post = cls(title=title, content=content, user_id=user_id)
        db.session.add(post)
        db.session.commit()

    def convert_time(self):
        test_date_format = '%Y-%m-%d %H:%M:%S.%f'
        strp_time = datetime.strptime(str(self.created_at), test_date_format)
        return strp_time.strftime("%a %b %d %Y, %H:%M %p")