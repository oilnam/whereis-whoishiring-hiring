import app
import unittest
from app.models import City, Job
import os

class BaseTestCase(unittest.TestCase):
    """ Base test case with throwaway, in-memory db """

    def create_app(self):
        app.config.from_object('config.TestConfiguration')
        return app

    def setUp(self):
        app.db.create_all()

    def tearDown(self):
        app.db.session.remove()
        app.db.drop_all()




if __name__ == '__main__':
    unittest.main()
