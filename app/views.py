from app import app, db
from flask import render_template, redirect, url_for
from sqlalchemy import func, desc
from models import City, Europe, Job, SEAsia, noCal, soCal
from helpers import magic, mapMonthToName, lastUpdate
from errors import not_found_error, internal_error

@app.route('/')
@app.route('/index')
@app.cache.cached(timeout=500)
def index():

    # harcoded variables; to be replaced when auto-update will be ready
    lastMonth = 10
    lastYear = 2015
    totalJobs = Job.query.count()

    top12cities = db.session.\
                  query(func.count(Job.description).label('noJobs'), City.name).\
                  join(City).\
                  filter(Job.month == lastMonth).\
                  filter(Job.year == lastYear).\
                  filter(City.country != '_intern_').\
                  group_by(City.name).\
                  order_by(desc('noJobs')).limit(12)

    top12countries = db.session.\
                     query(func.count(Job.description).label('noJobs'), City.country).\
                     join(City).\
                     filter(Job.month == lastMonth).\
                     filter(Job.year == lastYear).\
                     filter(City.country != '_intern_').\
                     group_by(City.country).\
                     order_by(desc('noJobs')).limit(12)

    europeJobs = db.session.query(Job.id).join(City).\
                 filter(City.country.in_(db.session.query(Europe.country))).\
                 filter(Job.month == lastMonth).\
                 filter(Job.year == lastYear).\
                 group_by(Job.hn_id).count()

    seasiaJobs = db.session.query(Job.id).join(City).\
                 filter(City.country.in_(db.session.query(SEAsia.country))).\
                 filter(Job.month == lastMonth).\
                 filter(Job.year == lastYear).\
                 group_by(Job.hn_id).count()

    noCalJobs = db.session.query(Job.id).join(City).\
                 filter(City.name.in_(db.session.query(noCal.city))).\
                 filter(Job.month == lastMonth).\
                 filter(Job.year == lastYear).\
                 group_by(Job.hn_id).count()

    soCalJobs = db.session.query(Job.id).join(City).\
                 filter(City.name.in_(db.session.query(soCal.city))).\
                 filter(Job.month == lastMonth).\
                 filter(Job.year == lastYear).\
                 group_by(Job.hn_id).count()

    remoteJobs = db.session.query(Job.id).join(City).\
                 filter(City.name == 'REMOTE').\
                 filter(Job.month == lastMonth).\
                 filter(Job.year == lastYear).\
                 group_by(Job.hn_id).count()

    internJobs = db.session.query(Job.id).join(City).\
                 filter(City.name == 'INTERN').\
                 filter(Job.month == lastMonth).\
                 filter(Job.year == lastYear).\
                 group_by(Job.hn_id).count()


    return render_template('index.html',
                           title = u'where is who is hiring? hiring?',
                           lastMonth = lastMonth,
                           lastMonthName = mapMonthToName(lastMonth),
                           lastYear = lastYear,
                           top12cities = top12cities,
                           top12countries = top12countries,
                           totalJobs = totalJobs,
                           europeJobs = europeJobs,
                           seasiaJobs = seasiaJobs,
                           noCalJobs = noCalJobs,
                           soCalJobs = soCalJobs,
                           remoteJobs = remoteJobs,
                           internJobs = internJobs,
                           lastUpdate = lastUpdate())


@app.route('/city/<year>/<month>')
@app.cache.cached(timeout=500)
def browse_cities_by_month(year = 0, month = 0):

    if int(month) not in range(1,13):
        return redirect(url_for('index'))

    totalRank = db.session.\
                query(func.count(Job.location).label('noJobs'), City.name).\
                join(City).\
                filter(Job.month == month).\
                filter(Job.year == year).\
                filter(City.country != '_intern_').\
                group_by(City.name).\
                order_by(desc('noJobs')).all()

    jobsNo = Job.query.filter_by(year = year, month = month).count()

    return render_template('browse_by_month.html',
                           title = u'wwh? | {0}-{1}'.format(month, year),
                           totalRank = magic(totalRank, []),
                           jobsNo = jobsNo,
                           currentMonth = mapMonthToName(int(month)),
                           year = year, month = month,
                           menuLink = 'country',
                           internalLink = 'city')


@app.route('/country/<year>/<month>')
@app.cache.cached(timeout=500)
def browse_countries_by_month(year = 0, month = 0):

    if int(month) not in range(1,13):
        return redirect(url_for('index'))

    totalRank = db.session.\
                query(func.count(Job.location).label('noJobs'), City.country).\
                join(City).\
                filter(Job.month == month).\
                filter(Job.year == year).\
                filter(City.country != '_intern_').\
                group_by(City.country).\
                order_by(desc('noJobs')).all()

    jobsNo = Job.query.filter_by(year = year, month = month).count()

    return render_template('browse_by_month.html',
                           title = u'wwh? | {0}-{1}'.format(month, year),
                           totalRank = magic(totalRank, []),
                           jobsNo = jobsNo,
                           currentMonth = mapMonthToName(int(month)),
                           year = year, month = month,
                           menuLink = 'city',
                           internalLink = 'country')


@app.route('/city/<year>/<month>/<city>')
@app.cache.cached(timeout=500)
def show_by_city(year, month, city):

    jobs = db.session.query(Job.description, Job.id, Job.hn_id).join(City).\
           filter(City.name == city).\
           filter(Job.month == month).\
           filter(Job.year == year).all()

    return render_template('show_place.html',
                           title = u'wwh? | {0} | {1}-{2}'.format(city, month, year),
                           place = city,
                           jobs = jobs, year = year,
                           month = mapMonthToName(int(month)))


@app.route('/country/<year>/<month>/<country>')
@app.cache.cached(timeout=500)
def show_by_country(year, month, country):

    jobs = db.session.query(Job.description, Job.id, Job.hn_id).join(City).\
           filter(City.country == country).\
           filter(Job.month == month).\
           filter(Job.year == year).all()

    return render_template('show_place.html',
                           title = u'wwh? | {0} | {1}-{2}'.format(country, month, year), 
                           place = country,
                           jobs = jobs, year = year,
                           month = mapMonthToName(int(month)))


@app.route('/europe/<year>/<month>')
@app.cache.cached(timeout=500)
def show_europe(year, month):

    jobs = db.session.query(Job.description, Job.id, Job.hn_id).\
           join(City).\
           filter(City.country.in_(db.session.query(Europe.country))).\
           filter(Job.month == month).\
           filter(Job.year == year).\
           group_by(Job.hn_id).all()

    return render_template('show_place.html',
                           title = u'wwh? | Europe | {0}-{1}'.format(month, year),
                           jobs = jobs, year = year,
                           month = mapMonthToName(int(month)),
                           place = 'Europe')


@app.route('/seasia/<year>/<month>')
@app.cache.cached(timeout=500)
def show_seasia(year, month):

    jobs = db.session.query(Job.description, Job.id, Job.hn_id).\
           join(City).\
           filter(City.country.in_(db.session.query(SEAsia.country))).\
           filter(Job.month == month).\
           filter(Job.year == year).\
           group_by(Job.hn_id).all()

    return render_template('show_place.html',
                           title = u'wwh? | SE Asia | {0}-{1}'.format(month, year),
                           jobs = jobs, year = year,
                           month = mapMonthToName(int(month)),
                           place = 'SE Asia')


@app.route('/nocal/<year>/<month>')
@app.cache.cached(timeout=500)
def show_nocal(year, month):

    jobs = db.session.query(Job.description, Job.id, Job.hn_id).\
           join(City).\
           filter(City.name.in_(db.session.query(noCal.city))).\
           filter(Job.month == month).\
           filter(Job.year == year).\
           group_by(Job.hn_id).all()

    return render_template('show_place.html',
                           title = u'wwh? | NO Cal | {0}-{1}'.format(month, year),
                           jobs = jobs, year = year,
                           month = mapMonthToName(int(month)),
                           place = 'Northern California')


@app.route('/socal/<year>/<month>')
@app.cache.cached(timeout=500)
def show_socal(year, month):

    jobs = db.session.query(Job.description, Job.id, Job.hn_id).\
           join(City).\
           filter(City.name.in_(db.session.query(soCal.city))).\
           filter(Job.month == month).\
           filter(Job.year == year).\
           group_by(Job.hn_id).all()

    return render_template('show_place.html',
                           title = u'wwh? | SO Cal | {0}-{1}'.format(month, year),
                           jobs = jobs, year = year,
                           month = mapMonthToName(int(month)),
                           place = 'Southern California')


@app.route('/all/cities')
@app.cache.cached(timeout=500)
def all_cities():

    allCities = db.session.\
                query(func.count(Job.description).label('noJobs'), City.name).\
                join(City).\
                filter(City.country != '_intern_').\
                group_by(City.name).\
                order_by(desc('noJobs')).all()

    return render_template('all_cities.html',
                           title = u'wwh? | all cities',
                           allCities = allCities)


@app.route('/all/countries')
@app.cache.cached(timeout=500)
def all_countries():

    allCountries = db.session.\
                   query(func.count(Job.description).label('noJobs'), City.country).\
                   join(City).\
                   filter(City.country != '_intern_').\
                   group_by(City.country).\
                   order_by(desc('noJobs')).all()

    return render_template('all_countries.html',
                           title = u'wwh? | all countries',
                           allCountries = allCountries)


@app.route('/faq')
@app.cache.cached(timeout=500)
def faq():
    
    return render_template('faq.html', title = u'wwh? | faq')
