import unittest
import time
from app import create_app, db
from app.models import User


class ModelUserTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        user = User(password='password')
        self.assertTrue(user.password_hash is not None)

    def test_no_password_getter(self):
        user = User(password='password')
        with self.assertRaises(AttributeError):
            user.password

    def test_password_verification(self):
        user = User(password='password')
        self.assertTrue(user.verify_password('password'))
        self.assertFalse(user.verify_password('pa$$w0rd'))

    def test_password_salting(self):
        user = User(password='password')
        user2 = User(password='pa$$w0rd')
        self.assertTrue(user.password_hash != user2.password_hash)

    def test_valid_confirmation_token(self):
        user = User(password='password')
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        self.assertTrue(user.confirm(token))

    def test_invalid_confirmation_token(self):
        user = User(password='password')
        user2 = User(password='pa$$w0rd')
        db.session.add(user)
        db.session.add(user2)
        db.session.commit()
        token = user.generate_confirmation_token()
        self.assertFalse(user2.confirm(token))

    def test_expired_confirmation_token(self):
        user = User(password='password')
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token(1)
        time.sleep(2)
        self.assertFalse(user.confirm(token))

    def test_valid_reset_token(self):
        user = User(password='password')
        db.session.add(user)
        db.session.commit()
        token = user.generate_password_reset_token()
        self.assertTrue(User.reset_password(token, 'pa$$w0rd'))
        self.assertTrue(user.verify_password('pa$$w0rd'))

    def test_invalid_reset_token(self):
        user = User(password='password')
        db.session.add(user)
        db.session.commit()
        token = user.generate_password_reset_token()
        self.assertFalse(User.reset_password(token + '0', 'pa$$w0rd'))
        self.assertTrue(user.verify_password('password'))

    def test_valid_email_change_token(self):
        user = User(email='ta@utdallas.edu', password='password')
        db.session.add(user)
        db.session.commit()
        token = user.generate_email_change_token('student@utdallas.edu')
        self.assertTrue(user.change_email(token))
        self.assertTrue(user.email == 'student@utdallas.edu')

    def test_invalid_email_change_token(self):
        user1 = User(email='ta@utdallas.edu', password='password')
        user2 = User(email='student@utdallas.edu', password='pa$$w0rd')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        token = user1.generate_email_change_token('professor@utdallas.edu')
        self.assertFalse(user2.change_email(token))
        self.assertTrue(user2.email == 'student@utdallas.edu')

    def test_duplicate_email_change_token(self):
        user1 = User(email='ta@utdallas.edu', password='password')
        user2 = User(email='student@utdallas.edu', password='pa$$w0rd')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        token = user2.generate_email_change_token('ta@utdallas.edu')
        self.assertFalse(user2.change_email(token))
        self.assertTrue(user2.email == 'student@utdallas.edu')
