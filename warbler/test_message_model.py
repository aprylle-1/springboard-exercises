from email.mime import image
import os
from re import M
from threading import currentThread
from unittest import TestCase

from models import db, User, Message, Follows

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import CURR_USER_KEY, app

app.config['WTF_CSRF_ENABLED'] = False

db.create_all()

class MessageModelTestCase(TestCase):
    """Test Model for Messages"""

    def setUp(self):

        db.drop_all()
        db.create_all()

        user = User.signup(username="user", password="password", email="email@email.com", image_url=None)
        user_id = 1111
        user.id = user_id

        db.session.commit()

        self.user = user
        self.user_id = user_id

    def tearDown(self):

        db.session.rollback()

    def test_message_model(self):
        """Test if Message Model Works"""

        text = "This is a test message"

        message = Message(text=text, user_id=self.user_id)
        message_id = 1111
        message.id = message_id

        db.session.add(message)
        db.session.commit()

        get_message = Message.query.get(message_id)
        user = User.query.get(self.user_id)

        self.assertEqual(text, get_message.text)
        self.assertEqual(user, get_message.user)
