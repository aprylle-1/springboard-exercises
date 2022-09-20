from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User model"""

    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    feedbacks = db.relationship("Feedback", backref="user")

    def __repr__(self):
        return f"<User - {self.username}>"


    @classmethod
    def create_user(cls, username, password, email, first_name, last_name):
        """Class method that creates a user and saves it to the database"""

        hashed = bcrypt.generate_password_hash(password)

        hashed_utf = hashed.decode("utf8")
            
        return cls(username=username, password=hashed_utf, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def login_user(cls, username, password):
        """Login User"""

        try:
            user = cls.query.filter(cls.username == username).one()
            if user and bcrypt.check_password_hash(user.password, password):
                return user
            else:
                return False
        
        except:
            return None

class Feedback(db.Model):
    """Feedback Model"""

    __tablename__ = "feedbacks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.ForeignKey("users.username"), nullable=False)

    def __repr__(self):
        return f"<Feedback {self.id} - {self.title}>" 