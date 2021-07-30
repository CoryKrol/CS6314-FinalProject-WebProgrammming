import re
import unittest
from app import create_app, db
from app.models import User, Role


class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'NPC' in response.data)

    def test_register_and_login(self):
        # Register new account
        response = self.client.post('/auth/register', data={
            'email': 'student@utdallas.edu',
            'username': 'student',
            'password': 'password',
            'password2': 'password'
        })
        self.assertEqual(response.status_code, 302)

        # Login with new account
        response = self.client.post('/auth/login', data={
            'email': 'student@utdallas.edu',
            'password': 'password'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(re.search(b'Hello,\s+student!', response.data))
        self.assertTrue(
            b'You have not confirmed your account yet' in response.data)

        # Send confirmation token
        user = User.query.filter_by(email='student@utdallas.edu').first()
        token = user.generate_account_confirmation_token()
        response = self.client.get('/auth/confirmation/{}'.format(token),
                                   follow_redirects=True)
        user.confirm(token)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            b'Account created successfully.' in response.data)

        # Logout
        response = self.client.get('/auth/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'You are now logged out.' in response.data)
