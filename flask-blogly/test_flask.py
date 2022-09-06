from unittest import TestCase

from app import app
from models import db, User, default_img

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///test_blogly'
app.config["SQLALCHEMY_ECHO"] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCast(TestCase):
    """Tests For All Views in Blogly App"""

    def setUp(self):
        """Add a Sample User"""

        #delete all users
        User.query.delete()
        user_id = User.add_user(first_name="SampleUser", last_name="SampleLastName")
        user = User.query.get(user_id)
        self.user_id = user_id
        self.first_name = user.first_name
        self.last_name = user.last_name

    def tearDown(self):
        """Clean up fouled up transaction"""

        db.session.rollback()

    def test_list_all_users(self):
        """Test Show All Users View"""
        with app.test_client() as client:
            
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"{self.first_name} {self.last_name}", html)
        
    def test_show_create_user_form(self):
        """Test Show Create User Form"""
        with app.test_client() as client:

            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Create User</h1>", html)

    def test_create_user(self):
        """Test Create User Route"""

        with app.test_client() as client:
            data = {"first_name" : "SampleUser2", "last_name" : "SampleLastName2", "image_url" : default_img}
            
            resp = client.post("/users/new", data = data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("SampleUser2 SampleLastName2", html)

    def test_show_user_details(self):
        """Test Show User Detail Route"""

        with app.test_client() as client:
            
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<h1>{self.first_name} {self.last_name}</h1>', html)
