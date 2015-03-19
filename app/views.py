from app import app, db
import flask
from sqlalchemy import func, desc
from models import City, Job
from helpers import magic, mapMonths
from errors import not_found_error, internal_error

@app.route('/')
@app.route('/index')
def index():

    lastMonth = 3
    lastYear = 2015
    totalJobs = Job.query.count()

    lastRank = db.session.\
               query(func.count(Job.description).label('noJobs'), City.name).\
               join(City).\
               filter(Job.month == '3').\
               filter(Job.year == '2015').\
               group_by(City.name).\
               order_by(desc('noJobs')).limit(12)

    lastRankCountry = db.session.\
                      query(func.count(Job.description).label('noJobs'), City.country).\
                      join(City).\
                      filter(Job.month == '3').\
                      filter(Job.year == '2015').\
                      group_by(City.country).\
                      order_by(desc('noJobs')).limit(12)

    topCities = db.session.\
                query(func.count(Job.description).label('noJobs'), City.name).\
                join(City).\
                group_by(City.name).\
                order_by(desc('noJobs')).limit(12)

    return flask.render_template('index.html',
                                 title = 'who is hiring?',
                                 topCities = topCities,
                                 lastMonth = lastMonth,
                                 lastYear = lastYear,
                                 lastRank = lastRank,
                                 lastRankCountry = lastRankCountry,
                                 totalJobs = totalJobs)


@app.route('/city/<year>/<month>')
def browse_cities_by_month(year = 0, month = 0):

    if int(month) not in range(1,13):
        return flask.redirect(flask.url_for('index'))

    totalRank = db.session.\
                query(func.count(Job.location).label('noJobs'), City.name).\
                join(City).\
                filter(Job.month == month).\
                filter(Job.year == year).\
                group_by(City.name).\
                order_by(desc('noJobs')).all()

    jobsNo = Job.query.filter_by(year = year, month = month).count()

    return flask.render_template('browse_city_by_month.html',
                                 title = 'who is hiring?',
                                 totalRank = magic(totalRank, []),
                                 jobsNo = jobsNo,
                                 currentMonth = mapMonths(int(month)),
                                 year = year, month = month)


@app.route('/country/<year>/<month>')
def browse_countries_by_month(year = 0, month = 0):

    if int(month) not in range(1,13):
        return flask.redirect(flask.url_for('index'))

    totalRank = db.session.\
                query(func.count(Job.location).label('noJobs'), City.country).\
                join(City).\
                filter(Job.month == month).\
                filter(Job.year == year).\
                group_by(City.country).\
                order_by(desc('noJobs')).all()

    jobsNo = Job.query.filter_by(year = year, month = month).count()

    return flask.render_template('browse_country_by_month.html',
                                 title = 'who is hiring?',
                                 totalRank = magic(totalRank, []),
                                 jobsNo = jobsNo,
                                 currentMonth = mapMonths(int(month)),
                                 year = year, month = month)


@app.route('/city/<year>/<month>/<city>')
def browse_by_city(year, month, city):

    jobs = db.session.query(Job.description).join(City).\
           filter(City.name == city).\
           filter(Job.month == month).\
           filter(Job.year == year).all()

    return flask.render_template('show_city.html',
                                 title = city, city = city,
                                 jobs = jobs, year = year,
                                 month = mapMonths(int(month)))


@app.route('/country/<year>/<month>/<country>')
def browse_by_country(year, month, country):

    jobs = db.session.query(Job.description).join(City).\
           filter(City.country == country).\
           filter(Job.month == month).\
           filter(Job.year == year).all()

    return flask.render_template('show_country.html',
                                 title = country, country = country,
                                 jobs = jobs, year = year,
                                 month = mapMonths(int(month)))


@app.route('/all/cities')
def all_cities():

    allCities = db.session.\
                query(func.count(Job.description).label('noJobs'), City.name).\
                join(City).\
                group_by(City.name).\
                order_by(desc('noJobs')).all()

    return flask.render_template('all_cities.html',
                                 title = 'all cities',
                                 allCities = allCities)

@app.route('/all/countries')
def all_countries():

    allCountries = db.session.\
                   query(func.count(Job.description).label('noJobs'), City.country).\
                   join(City).\
                   group_by(City.country).\
                   order_by(desc('noJobs')).all()

    return flask.render_template('all_countries.html',
                                 title = 'all countries',
                                 allCountries = allCountries)
