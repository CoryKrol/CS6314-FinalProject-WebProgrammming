import unittest
import time
from datetime import datetime

from app import create_app, db
from app.models import AnonymousUser, Follow, Permission, Role, Stock, User


class ModelStockTest(unittest.TestCase):
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

    def test_is_watched_by(self):
        # Assert user not watching stock
        user = User(email='student@utdallas.edu', password='password')
        stock = Stock(name='Apple', ticker='AAPL', sector="Tech", is_active=True, year_high=1000.0, year_low=100.0)
        db.session.add(user)
        db.session.add(stock)
        db.session.commit()
        self.assertFalse(user.is_watching(stock))
        self.assertFalse(stock.is_watched_by(user))
