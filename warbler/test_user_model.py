"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        #creating user 1 and setting their user id to a user known number
        user1 = User.signup(username="user1", password="password", image_url=None, email='user1@email.com')
        user1_id = 11
        user1.id = user1_id

        #creating user 2 and setting their user id to a user known number
        user2 = User.signup(username="user2", password="password", image_url=None, email='user2@email.com')
        user2_id = 22
        user2.id = user2_id

        db.session.commit()

        self.user1 = user1
        self.user1_id = user1_id

        self.user2 = user2
        self.user2_id = user2_id

        self.client = app.test_client()

    def tearDown(self):
        """Steps done after every test case is run"""

        db.session.rollback()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)


    def test_check_followers_following(self):
        """Check if db.relationship followers/following work"""

        follow = Follows(user_being_followed_id = self.user2_id, user_following_id = self.user1_id)

        db.session.add(follow)
        db.session.commit()

        # get user1 details from database

        user1 = User.query.get(self.user1_id)
        user2 = User.query.get(self.user2.id)

        #user 1 should have no followers but have 1 following user
        self.assertEqual(len(user1.followers), 0)
        self.assertEqual(len(user1.following), 1)

        # user 2 should have 1 follower and 0 following user
        self.assertEqual(len(user2.followers), 1)
        self.assertEqual(len(user2.following), 0)

    def test_user_messages(self):
        """Check if db.messages relationship works"""

        message = "this is a test message"
        new_message = Message(user_id=self.user1_id, text=message)

        db.session.add(new_message)
        db.session.commit()

        user1 = User.query.get(self.user1_id)

        self.assertEqual(len(user1.messages), 1)
        self.assertEqual(user1.messages[0].text, message)

    def test_is_followed_by(self):
        """Check if method is_followed_by works"""

        follow = Follows(user_being_followed_id = self.user2_id, user_following_id = self.user1_id)

        db.session.add(follow)
        db.session.commit()

        user1 = User.query.get(self.user1_id)
        user2 = User.query.get(self.user2_id)

        self.assertEqual(user1.is_followed_by(user2), False)
        self.assertEqual(user2.is_followed_by(user1), True)

    def test_is_following(self):
        """Check if method is_following works"""

        follow = Follows(user_being_followed_id = self.user2_id, user_following_id = self.user1_id)

        db.session.add(follow)
        db.session.commit()

        user1 = User.query.get(self.user1_id)
        user2 = User.query.get(self.user2_id)

        self.assertEqual(user1.is_following(user2), True)
        self.assertEqual(user2.is_following(user1), False)

    def test_repr(self):
        """Check if repr works"""

        new_user = User.signup(username="new_user", password="password", image_url=None, email='new_user@email.com')
        new_user_id = 123456
        new_user.id = new_user_id
        db.session.commit()

        self.assertEqual(str(new_user),f"<User #{new_user_id}: new_user, new_user@email.com>")