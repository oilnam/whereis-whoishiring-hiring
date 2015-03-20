from app import app, db
from flask import render_template, redirect, url_for
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

    return render_template('index.html',
                           title = 'where is who is hiring? hiring?',
                           topCities = topCities,
                           lastMonth = lastMonth,
                           lastYear = lastYear,
                           lastRank = lastRank,
                           lastRankCountry = lastRankCountry,
                           totalJobs = totalJobs)


@app.route('/city/<year>/<month>')
def browse_cities_by_month(year = 0, month = 0):

    if int(month) not in range(1,13):
        return redirect(url_for('index'))

    totalRank = db.session.\
                query(func.count(Job.location).label('noJobs'), City.name).\
                join(City).\
                filter(Job.month == month).\
                filter(Job.year == year).\
                group_by(City.name).\
                order_by(desc('noJobs')).all()

    jobsNo = Job.query.filter_by(year = year, month = month).count()

    return render_template('browse_city_by_month.html',
                           title = 'wiwihi? | {0}-{1}'.format(month, year),
                           totalRank = magic(totalRank, []),
                           jobsNo = jobsNo,
                           currentMonth = mapMonths(int(month)),
                           year = year, month = month)


@app.route('/country/<year>/<month>')
def browse_countries_by_month(year = 0, month = 0):

    if int(month) not in range(1,13):
        return redirect(url_for('index'))

    totalRank = db.session.\
                query(func.count(Job.location).label('noJobs'), City.country).\
                join(City).\
                filter(Job.month == month).\
                filter(Job.year == year).\
                group_by(City.country).\
                order_by(desc('noJobs')).all()

    jobsNo = Job.query.filter_by(year = year, month = month).count()

    return render_template('browse_country_by_month.html',
                           title = 'wiwihi? | {0}-{1}'.format(month, year),
                           totalRank = magic(totalRank, []),
                           jobsNo = jobsNo,
                           currentMonth = mapMonths(int(month)),
                           year = year, month = month)


@app.route('/city/<year>/<month>/<city>')
def show_by_city(year, month, city):

    jobs = db.session.query(Job.description, Job.id).join(City).\
           filter(City.name == city).\
           filter(Job.month == month).\
           filter(Job.year == year).all()

    return render_template('show_city.html',
                           title = 'wiwihi? | {0} | {1}-{2}'.format(city, month, year), 
                           city = city,
                           jobs = jobs, year = year,
                           month = mapMonths(int(month)))


@app.route('/country/<year>/<month>/<country>')
def show_by_country(year, month, country):

    jobs = db.session.query(Job.description, Job.id).join(City).\
           filter(City.country == country).\
           filter(Job.month == month).\
           filter(Job.year == year).all()

    return render_template('show_country.html',
                           title = 'wiwihi? | {0} | {1}-{2}'.format(country, month, year), 
                           country = country,
                           jobs = jobs, year = year,
                           month = mapMonths(int(month)))


@app.route('/all/cities')
def all_cities():

    allCities = db.session.\
                query(func.count(Job.description).label('noJobs'), City.name).\
                join(City).\
                group_by(City.name).\
                order_by(desc('noJobs')).all()

    return render_template('all_cities.html',
                           title = 'wiwihi? | all cities',
                           allCities = allCities)

@app.route('/all/countries')
def all_countries():

    allCountries = db.session.\
                   query(func.count(Job.description).label('noJobs'), City.country).\
                   join(City).\
                   group_by(City.country).\
                   order_by(desc('noJobs')).all()

    return render_template('all_countries.html',
                           title = 'wiwihi? | all countries',
                           allCountries = allCountries)
