from unittest import TestCase

from app import app
from models import db, User, Post, default_img

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
        Post.query.delete()
        User.query.delete()
        user_id = User.add_user(first_name="SampleUser", last_name="SampleLastName")
        post = Post(title="Test Title", content="This is a test post", user_id = user_id)
        db.session.add(post)
        db.session.commit()
        user = User.query.get(user_id)
        self.post = post
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

    def test_show_edit_user_form(self):
        """Test for route that creates the edit form"""

        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<input type="text" name="first_name" value="SampleUser">', html)
    
    def test_edit_user(self):
        """Test for Create User functionality"""

        with app.test_client() as client:
            data = {"first_name" : "Will", "last_name" : "Asuna", "image_url" : ""}
            resp = client.post(f"/users/{self.user_id}/edit", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Will Asuna", html)

    def test_edit_user_with_invalid_fields(self):  
        """Test for Create User functionality with invalid fields"""

        with app.test_client() as client:
            data = {"first_name" : "", "last_name" : "", "image_url" : ""}
            resp = client.post(f"/users/{self.user_id}/edit", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("You have not entered a new first name", html)
            self.assertIn("You have not entered a new last name", html)

            data = {"first_name" : "adsasjkldjaskldjlasdjklasjdklasjdklasjkldjklasdjklasjdklasjkldjaskldjklasdjklasjldkasjlkdjklasdjklasdjklasdjklasjdlkasjkldas", "last_name" : "adsasjkldjaskldjlasdjklasjdklasjdklasjkldjklasdjklasjdklasjkldjaskldjklasdjklasjldkasjlkdjklasdjklasdjklasdjklasjdlkasjkldas", "image_url" : ""}

            resp = client.post(f"/users/{self.user_id}/edit", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("First Name must be 50 characters only", html)
            self.assertIn("Last Name must be 50 characters only", html)

    def test_delete_user(self):
        """Test delete user function"""
        Post.query.delete()
        with app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/delete" ,follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertNotIn("SampleUser", html)
            self.assertNotIn("SampleLastName", html)


    def test_get_add_post_form(self):
        """Test show add test form function/route"""

        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/posts/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Add Post for SampleUser SampleLastName", html)
    
    
    def test_add_post_for_user(self):
        """Test add post function/route"""

        with app.test_client() as client:
            data = {"title" : "Test Post", "content" : "This is a Test Case"}
            resp = client.post(f"/users/{self.user_id}/posts/new", data=data, follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test Post", html)

    def test_show_post_details(self):
        """Test route that displays post information"""

        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("This is a test post", html)
            self.assertIn("Test Title", html)
    
    def test_get_edit_post_form(self):
        """Test route that obtains/generates the Post Edit Form"""

        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test Title", html)

    def test_edit_post(self):
        """Test route that edits posts"""
        data = {"title" : "This is an edited title", "content" : "Edited test content"}

        with app.test_client() as client:
            resp = client.post(f"/posts/{self.post.id}/edit", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("This is an edited title", html)

    def test_edit_post_with_invalid_input(self):
        """Test route that edits posts using invalid inputs"""

        data = {"title" : "", "content" : ""}

        with app.test_client() as client:
            resp = client.post(f"/posts/{self.post.id}/edit", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Missing Post Title", html)
            self.assertIn("Missing Post Content Details", html)

    def test_delete_post(self):

        with app.test_client() as client:
            resp = client.post(f"/posts/{self.post.id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Test Title", html)
