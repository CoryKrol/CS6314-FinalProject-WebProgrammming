import unittest
import json
import re
from base64 import b64encode
from app import create_app, db
from app.models import User, Role, Stock, Trade


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_headers(self, username, password):
        return {
            'Authorization': 'Basic ' + b64encode((username + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_404(self):
        response = self.client.get('/incorrect', headers=self.get_api_headers('email', 'password'))
        self.assertEqual(response.status_code, 404)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['error'], 'not found')

    def test_no_auth(self):
        response = self.client.get('/api/v1/trades/', content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_bad_auth(self):
        # Add user
        role = Role.query.filter_by(name='User').first()
        self.assertIsNotNone(role)
        user = User(email='student@utdallas.edu', password='password', confirmed=True, role=role)
        db.session.add(user)
        db.session.commit()

        # Authenticate with incorrect password
        response = self.client.get('/api/v1/trades/', headers=self.get_api_headers('student@utdallas.edu', 'pa$$w0rd'))
        self.assertEqual(response.status_code, 401)

    def test_token_auth(self):
        # Add user
        role = Role.query.filter_by(name='User').first()
        self.assertIsNotNone(role)
        user = User(email='student@utdallas.edu', password='password', confirmed=True, role=role)
        db.session.add(user)
        db.session.commit()

        # Issue request with incorrect token
        response = self.client.get('/api/v1/trades/', headers=self.get_api_headers('incorrect-token', ''))
        self.assertEqual(response.status_code, 401)

        # Get token
        response = self.client.post('/api/v1/tokens/', headers=self.get_api_headers('student@utdallas.edu', 'password'))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(json_response.get('token'))
        token = json_response['token']

        # Issue request with token
        response = self.client.get('/api/v1/trades/', headers=self.get_api_headers(token, ''))
        self.assertEqual(response.status_code, 200)

    def test_anonymous(self):
        response = self.client.get('/api/v1/trades/', headers=self.get_api_headers('', ''))
        self.assertEqual(response.status_code, 401)

    def test_unconfirmed_account(self):
        # Add unconfirmed user
        role = Role.query.filter_by(name='User').first()
        self.assertIsNotNone(role)
        user = User(email='student@utdallas.edu', password='password', confirmed=False, role=role)
        db.session.add(user)
        db.session.commit()

        # Get list of trades with unconfirmed account
        response = self.client.get('/api/v1/trades/', headers=self.get_api_headers('student@utdallas.edu', 'password'))
        self.assertEqual(response.status_code, 403)

    def test_trades(self):
        # Add user
        role = Role.query.filter_by(name='User').first()
        self.assertIsNotNone(role)
        user1 = User(username='student', email='student@utdallas.edu', password='password', confirmed=True, role=role)
        user2 = User(username='ta', email='ta@utdallas.edu', password='pa$$w0rd', confirmed=True, role=role)
        stock1 = Stock(name='Apple', ticker='AAPL', sector="Tech", is_active=True, year_high=1000.0, year_low=100.0)
        stock2 = Stock(name='Nokia', ticker='NOK', sector="Tech", is_active=True, year_high=1000.0, year_low=100.0)
        db.session.add_all([user1, user2])
        user2.follow(user1)
        db.session.add_all([stock1, stock2, user1, user2])
        db.session.commit()

        # Create empty trade
        response = self.client.post(
            '/api/v1/trades/',
            headers=self.get_api_headers('student@utdallas.edu', 'password'),
            data=json.dumps({'stock': '', 'user': '', 'quantity': '', 'price': ''}))
        self.assertEqual(response.status_code, 400)

        # Create trade
        response = self.client.post(
            '/api/v1/trades/',
            headers=self.get_api_headers('student@utdallas.edu', 'password'),
            data=json.dumps({'stock': stock1.ticker, 'user': user1.username, 'quantity': 1, 'price': 1.0}))
        self.assertEqual(response.status_code, 201)
        url = response.headers.get('Location')
        self.assertIsNotNone(url)

        # Get new trade
        response = self.client.get(
            url,
            headers=self.get_api_headers('student@utdallas.edu', 'password'))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual('http://localhost' + json_response['url'], url)
        self.assertEqual(json_response['stock'], stock1.ticker)
        self.assertEqual(json_response['user'], user1.username)
        self.assertEqual(json_response['quantity'], 1)
        self.assertEqual(json_response['price'], 1.0)
        json_trade = json_response

        # Get trade from the user
        response = self.client.get(
            '/api/v1/users/{}/trades/'.format(user1.id),
            headers=self.get_api_headers('student@utdallas.edu', 'password'))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(json_response.get('trades'))
        self.assertEqual(json_response.get('count', 0), 1)
        self.assertEqual(json_response['trades'][0], json_trade)

        # Get the trade from the user as a follower
        response = self.client.get(
            '/api/v1/users/{}/timeline/'.format(user2.id),
            headers=self.get_api_headers('ta@utdallas.edu', 'pa$$w0rd'))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(json_response.get('trades'))
        self.assertEqual(json_response.get('count', 0), 1)
        self.assertEqual(json_response['trades'][0], json_trade)

        # Edit trade
        response = self.client.put(
            url,
            headers=self.get_api_headers('student@utdallas.edu', 'password'),
            data=json.dumps({'stock': stock2.ticker, 'user': user1.username, 'quantity': 3, 'price': 3.0}))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual('http://localhost' + json_response['url'], url)
        self.assertEqual(json_response['stock'], 'NOK')
        self.assertEqual(json_response['quantity'], 3)
        self.assertEqual(json_response['price'], 3.0)

    def test_users(self):
        # Add 2 users
        role = Role.query.filter_by(name='User').first()
        self.assertIsNotNone(role)
        user1 = User(email='student@utdallas.edu', username='student', password='password', confirmed=True, role=role)
        user2 = User(email='ta@utdallas.edu', username='ta', password='pa$$w0rd', confirmed=True, role=role)
        db.session.add_all([user1, user2])
        db.session.commit()

        # Get users
        response = self.client.get(
            '/api/v1/users/{}'.format(user1.id),
            headers=self.get_api_headers('ta@utdallas.edu', 'pa$$w0rd'))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['username'], 'student')
        response = self.client.get(
            '/api/v1/users/{}'.format(user2.id),
            headers=self.get_api_headers('ta@utdallas.edu', 'pa$$w0rd'))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['username'], 'ta')