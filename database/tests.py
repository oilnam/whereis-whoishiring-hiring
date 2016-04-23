from flask.ext.testing import TestCase
import os
import subprocess
import sys
import unittest

dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(dir)
from app import app, db
from app.models import City, Job

from full_hn_reindex import process_page
from index_cities import index_cities


class BaseTestCase(TestCase):
    """ Base test case """

    def create_app(self):
        app.config.from_object('config.TestConfiguration')
        return app

    def setUp(self):
        db.create_all()
        index_cities()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        subprocess.call('rm ../test.db', shell=True)


class IndexCities(BaseTestCase):
    def test_cities_are_indexed(self):
        assert City.query.filter(City.name == u'REMOTE').count() == 1
        assert City.query.filter(City.name == u'San Francisco').count() == 1


class IndexJobs(BaseTestCase):
    def test_full_integration(self):
        # since processing the page takes ~8 sec all tests are crammed in here

        process_page(123, update=False, localPage='resources/pages/072015.html')
        assert Job.query.filter(Job.month == 07, Job.year == 2015).count() == 1158

        # manually refine the db
        subprocess.call('sqlite3 ../test.db < refine_db.sql', shell=True)

        # check cities
        assert Job.query.filter(Job.month == 07, Job.year == 2015).count() == 1072
        assert Job.query.join(City).filter(City.name == u'REMOTE', Job.month == 07, Job.year == 2015).count() == 101
        assert Job.query.join(City).filter(City.name == u'San Francisco', Job.month == 07, Job.year == 2015).count() == 194
        assert Job.query.join(City).filter(City.name == u'London', Job.month == 07, Job.year == 2015).count() == 64
        assert Job.query.join(City).filter(City.name == u'Zurich', Job.month == 07, Job.year == 2015).count() == 5

        # check countries
        assert Job.query.join(City).filter(City.country == u'United States', Job.month == 07, Job.year == 2015).count() == 700
        assert Job.query.join(City).filter(City.country == u'United Kingdom', Job.month == 07, Job.year == 2015).count() == 78
        assert Job.query.join(City).filter(City.country == u'Singapore', Job.month == 07, Job.year == 2015).count() == 7

        # update page; all the results should stay the same
        process_page(123, update=True, localPage='resources/pages/072015.html')
        subprocess.call('sqlite3 ../test.db < refine_db.sql', shell=True)

        # check cities
        assert Job.query.filter(Job.month == 07, Job.year == 2015).count() == 1072
        assert Job.query.join(City).filter(City.name == u'REMOTE', Job.month == 07, Job.year == 2015).count() == 101
        assert Job.query.join(City).filter(City.name == u'San Francisco', Job.month == 07, Job.year == 2015).count() == 194
        assert Job.query.join(City).filter(City.name == u'London', Job.month == 07, Job.year == 2015).count() == 64
        assert Job.query.join(City).filter(City.name == u'Zurich', Job.month == 07, Job.year == 2015).count() == 5

        # check countries
        assert Job.query.join(City).filter(City.country == u'United States', Job.month == 07, Job.year == 2015).count() == 700
        assert Job.query.join(City).filter(City.country == u'United Kingdom', Job.month == 07, Job.year == 2015).count() == 78
        assert Job.query.join(City).filter(City.country == u'Singapore', Job.month == 07, Job.year == 2015).count() == 7


if __name__ == '__main__':
    unittest.main()

