from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for users."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user = User(first_name="Test", last_name="User", image_url="https://i.pinimg.com/736x/39/d3/e0/39d3e06ebb09a79f805356b9db516078.jpg")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user_first_name = user.first_name
        self.user_last_name = user.last_name

    def tearDown(self):
        """Clean any fouled transaction."""

        db.session.rollback()

    def test_root(self):
        with app.test_client() as client:
            resp = client.get("/", follow_redirects=True)
            html = resp.get_data(as_text=True)   

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Users', html)     

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Add User', html)

    def test_new_user_form(self):
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<button>Add</button>', html)       

    def test_add_user(self):
        with app.test_client() as client:
            d = {"firstName": "Test", "lastName": "User", "imageURL": "https://i.pinimg.com/736x/39/d3/e0/39d3e06ebb09a79f805356b9db516078.jpg"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test User', html)

    def test_user_page(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"{self.user_first_name} {self.user_last_name}'s Page", html)  

                





        