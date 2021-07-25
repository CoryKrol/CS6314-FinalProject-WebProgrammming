import re
import threading
import time
import unittest
from selenium import webdriver
from app import create_app, db, fake
from app.models import Role, User


class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        # Start Chrome
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        try:
            cls.client = webdriver.Chrome(options=options)
        except:
            pass

        # Skip tests if browser not started
        if cls.client:
            # Create application
            cls.app = create_app('testing')
            cls.app_context = cls.app.app_context()
            cls.app_context.push()

            import logging
            logger = logging.getLogger('werkzeug')
            logger.setLevel("ERROR")

            # Create database and populate with data
            db.create_all()
            Role.insert_roles()
            fake.users(10)

            # Add administrator user
            admin_role = Role.query.filter_by(name='Administrator').first()
            admin = User(email='',
                         username='student', password='password',
                         role=admin_role, confirmed=True)
            db.session.add(admin)
            db.session.commit()

            # Start Flask server in a thread
            cls.server_thread = threading.Thread(target=cls.app.run,
                                                 kwargs={'debug': False})
            cls.server_thread.start()

            time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        if cls.client:
            # Stop the flask server and the browser
            cls.client.get('http://localhost:5000/shutdown')
            cls.client.quit()
            cls.server_thread.join()

            # Destroy database
            db.drop_all()
            db.session.remove()

            # Remove application context
            cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest('Web browser not available')

    def tearDown(self):
        pass

    def test_admin_home_page(self):
        # Navigate to home
        self.client.get('http://localhost:5000/')
        self.assertTrue(re.search('Hello,\s+Stranger\s+!',
                                  self.client.page_source))

        # Navigate to login
        self.client.find_element_by_link_text('Log In').click()
        self.assertIn('<h1>Login</h1>', self.client.page_source)

        # Login
        self.client.find_element_by_name('email'). \
            send_keys('student@utdallas.edu')
        self.client.find_element_by_name('password').send_keys('password')
        self.client.find_element_by_name('submit').click()