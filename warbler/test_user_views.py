"""Test User Views"""

import os
from threading import currentThread
from unittest import TestCase

from models import db, User, Message, Follows

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import CURR_USER_KEY, app

app.config['WTF_CSRF_ENABLED'] = False

db.create_all()

class UserViewTestCase(TestCase):
    """Test Views for Users"""

    def setUp(self):
        """Create test client, add sample data"""

        db.drop_all()
        db.create_all()

        user1 = User.signup(username="user1", password="password", image_url=None, email='user1@email.com')
        user1_id = 11
        user1.id = user1_id

        user2 = User.signup(username="user2", password="password", image_url=None, email='user2@email.com')
        user2_id = 22
        user2.id = user2_id

        user3 = User.signup(username="user3", password="password", image_url=None, email='user3@email.com')
        user3_id = 33
        user3.id = user3_id

        db.session.commit()

        self.user1 = user1
        self.user1_id = user1_id

        self.user2 = user2
        self.user2_id = user2_id

        self.user3 = user3
        self.user3_id = user3_id

        self.client = app.test_client()

    def tearDown(self):

        db.session.rollback()

    def test_user_index(self):
        with self.client as client:
                
                resp = client.get("/users")

                html = resp.get_data(as_text=True)

                self.assertEqual(resp.status_code, 200)
                self.assertIn("@user1", html)
                self.assertIn("@user2", html)
                self.assertIn("@user3", html)

    def test_user_show(self):

        add_message = "This is a new message"

        message = Message(text=add_message, user_id=self.user1_id)
        db.session.add(message)
        db.session.commit()

        with self.client as client:

            resp = client.get(f"/users/{self.user1_id}")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(add_message, html)
            self.assertIn("@user1", html)

            #check that user does not have following/followers
            self.assertIn(f'<a href="/users/{self.user1_id}/following">0</a>', html)
            self.assertIn(f'<a href="/users/{self.user1_id}/followers">0</a>', html)

            #checks that only information about user is shown
            self.assertNotIn("@user2", html)

    def test_user_following(self):

        follow = Follows(user_being_followed_id = self.user2_id, user_following_id = self.user1_id)

        db.session.add(follow)
        db.session.commit()

        with self.client as client:
            with client.session_transaction() as session:

                session[CURR_USER_KEY] = self.user1_id

            resp = client.get(f"/users/{self.user1_id}/following", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("@user2", html)
            self.assertIn("Unfollow", html)

    def test_user_has_followers(self):

        follow = Follows(user_being_followed_id=self.user1_id, user_following_id = self.user2_id)
        db.session.add(follow)
        db.session.commit()

        with self.client as client:
            with client.session_transaction() as session:
                session[CURR_USER_KEY] = self.user1_id

            resp = client.get(f"/users/{self.user1_id}/followers", follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"@user2", html)
