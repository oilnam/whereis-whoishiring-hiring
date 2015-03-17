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


class DBConsistency(unittest.TestCase):
    """ Check the database is not messed up """

    def test_city_ids(self):
        assert City.query.filter_by(name = u'Z\xfcrich').first().id == 449
        assert City.query.filter_by(name = u'Zurich').first().id == 976
        assert City.query.filter_by(name = u'New York City').first().id == 173
        assert City.query.filter_by(name = u'New York').first().id == 968
        assert City.query.filter_by(name = u'SF').first().id == 971
        assert City.query.filter_by(name = u'San Francisco').first().id == 24
        assert City.query.filter_by(name = u'New Delhi').first().id == 739
        assert City.query.filter_by(name = u'Delhi').first().id == 960


if __name__ == '__main__':
    unittest.main()
