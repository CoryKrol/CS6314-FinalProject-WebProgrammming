import unittest
import time
from datetime import datetime

from app import create_app, db
from app.models import AnonymousUser, Permission, Role, User


class ModelUserTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()

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
            user.password()

    def test_password_verifipasswordion(self):
        user = User(password='password')
        self.assertTrue(user.verify_password('password'))
        self.assertFalse(user.verify_password('pa$$w0rd'))

    def test_password_salting(self):
        user = User(password='password')
        user2 = User(password='password')
        self.assertTrue(user.password_hash != user2.password_hash)

    def test_valid_account_confirmation_token(self):
        user = User(password='password')
        db.session.add(user)
        db.session.commit()
        token = user.generate_account_confirmation_token()
        self.assertTrue(user.confirm(token))

    def test_invalid_account_confirmation_token(self):
        user = User(password='password')
        user2 = User(password='pa$$w0rd')
        db.session.add(user)
        db.session.add(user2)
        db.session.commit()
        token = user.generate_account_confirmation_token()
        self.assertFalse(user2.confirm(token))

    def test_expired_confirmation_token(self):
        user = User(password='password')
        db.session.add(user)
        db.session.commit()
        token = user.generate_account_confirmation_token(1)
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

    def test_duplicate_password_email_change_token(self):
        user1 = User(email='ta@utdallas.edu', password='password')
        user2 = User(email='student@utdallas.edu', password='pa$$w0rd')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        token = user2.generate_email_change_token('ta@utdallas.edu')
        self.assertFalse(user2.change_email(token))
        self.assertTrue(user2.email == 'student@utdallas.edu')

    def test_user_role(self):
        user = User(email='student@utdallas.edu', password='password')
        self.assertTrue(user.can(Permission.FOLLOW))
        self.assertTrue(user.can(Permission.COMMENT))
        self.assertTrue(user.can(Permission.WRITE))
        self.assertFalse(user.can(Permission.MODERATE))
        self.assertFalse(user.can(Permission.ADMIN))

    @staticmethod
    def get_user_with_role(role):
        return User(email='student@utdallas.edu', password='password', role=role)

    def test_moderator_role(self):
        user = self.get_user_with_role(Role.query.filter_by(name='Moderator').first())
        self.assertTrue(user.can(Permission.FOLLOW))
        self.assertTrue(user.can(Permission.COMMENT))
        self.assertTrue(user.can(Permission.WRITE))
        self.assertTrue(user.can(Permission.MODERATE))
        self.assertFalse(user.can(Permission.ADMIN))

    def test_administrator_role(self):
        user = self.get_user_with_role(Role.query.filter_by(name='Administrator').first())
        self.assertTrue(user.can(Permission.FOLLOW))
        self.assertTrue(user.can(Permission.COMMENT))
        self.assertTrue(user.can(Permission.WRITE))
        self.assertTrue(user.can(Permission.MODERATE))
        self.assertTrue(user.can(Permission.ADMIN))

    def test_anonymous_user(self):
        user = AnonymousUser()
        self.assertFalse(user.can(Permission.FOLLOW))
        self.assertFalse(user.can(Permission.COMMENT))
        self.assertFalse(user.can(Permission.WRITE))
        self.assertFalse(user.can(Permission.MODERATE))
        self.assertFalse(user.can(Permission.ADMIN))

    def test_timestamps(self):
        user = User(password='password')
        db.session.add(user)
        db.session.commit()
        self.assertTrue(
            (datetime.utcnow() - user.member_since).total_seconds() < 3)
        self.assertTrue(
            (datetime.utcnow() - user.last_seen).total_seconds() < 3)

    def test_ping(self):
        user = User(password='password')
        db.session.add(user)
        db.session.commit()
        time.sleep(2)
        last_seen_before = user.last_seen
        user.ping()
        self.assertTrue(user.last_seen > last_seen_before)

    def test_gravatar(self):
        user = User(email='student@utdallas.edu', password='password')
        with self.app.test_request_context('/'):
            gravatar = user.gravatar()
            gravatar_256 = user.gravatar(size=256)
            gravatar_pg = user.gravatar(rating='pg')
            gravatar_retro = user.gravatar(default='retro')
        self.assertTrue('https://secure.gravatar.com/avatar/390415e449db6f9332c93dbb50a5f10d' in gravatar)
        self.assertTrue('s=256' in gravatar_256)
        self.assertTrue('r=pg' in gravatar_pg)
        self.assertTrue('d=retro' in gravatar_retro)
