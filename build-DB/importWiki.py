from bs4 import BeautifulSoup as bs
from sqlalchemy import update
import sys
import os
# this is a bit hackeryish. Should I rewrite everything in plain SQL?
dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(dir)
from app import db
from app.models import City

s = bs(open('wiki.html'))

table = s.find('table', class_ = 'wikitable')
rows = table.find_all('tr')

d = []
for i in range(1,len(rows)):
    city = rows[i].find_all('td')[2].get_text()
    country = rows[i].find_all('td')[4].find('a').string
    d.append( (city, country) )

# dump
for i in d:
    c = City(i[0], i[1])
    db.session.add(c)

db.session.commit()
db.session.close()

# replace ambiguous cities (see below)
City.query.filter_by(name = u'Cambridge').delete()
City.query.filter_by(name = u'Nice').delete()
City.query.filter_by(name = u'Mobile').delete()
City.query.filter_by(name = u'Pierre').delete()
City.query.filter_by(name = u'Lincoln').delete()
City.query.filter_by(name = u'Windsor').delete()

m = City.query.filter(City.name.like(u'%Mexico City')).first()
db.session.delete(m)

# ad-hoc customizations
extra = [
    (u'Mountain View', u'United States'), (u'San Mateo', u'United States'),
    (u'Santa Monica', u'United States'), (u'Santa Clara', u'United States'),
    (u'Cupertino', u'United States'), (u'Palo Alto', u'United States'),
    (u'Camarillo', u'United States'), (u'Los Altos', u'United States'),
    (u'Redwood', u'United States'), (u'Sunnyvale', u'United States'),
    (u'Emeryville', u'United States'), (u'Orange County', u'United States'),
    (u'Oakland', u'United States'), (u'Paoli, PA', u'United States'),
    (u'Mexico City', u'Mexico'), (u'Buenos Aires', u'Argentina'),
    (u'Hong Kong', u'HK'), (u'Leuven', u'Belgium'),
    (u'Mumbai', u'India'), (u'Berkeley', u'United States'),
    (u'Delhi', u'India'), (u'Waltham', u'United States'),
    (u'Naperville', u'United States'), (u'Harbor Springs', u'United States'),
    (u'Irvine', u'United States'), (u'Durham', u'United States'),
    (u'Chattanooga', u'United States'), (u'Redmond', u'United States'),
    (u'New York', u'United States'), (u'San Jose', u'United States'),
    (u'NYC', u'United States'), (u'SF', u'United States'),
    (u'LA, CA', u'United States'), (u'Bloomington', u'United States'),
    (u'Cambridge', u'United States'), (u'Cambridge, UK', u'United Kingdom'),
    (u'Zurich', u'Switzerland'), (u'Nice, France', u'France'),
    (u'Versailles', u'France'), (u'Iron Mountain', u'United States'),
    (u'Lincoln, NE', u'United States'), (u'Windsor, ON', u'United States'),
    (u'Mobile, AL', u'United States'), (u'Pierre, SD', u'United States'),
    (u'Trento', u'Italy'), (u'Taghazout', u'Morocco'),
    (u'Pasadena', u'United States'), (u'Menlo Park', u'United States'),
    (u'West Hollywood', u'United States'), (u'Chennai', u'India'),
    (u'Myrtle Beach', u'United States'), (u'Gurgaon', u'India'),
    (u'Culver City', u'United States'), (u'Frederick, MD', u'United States'),
    (u'Fort Worth', u'United States'), (u'Goettingen', u'Germany'),
    (u'Los Gatos', u'United States'), (u'Florianopolis', u'Brazil'),
    (u'Boca Raton', u'United States'), (u'Aliso Viejo', u'United States'),
    (u'Ann Arbor', u'United States'), (u'Newark', u'United States'),
    (u'New Haven', u'United States'), (u'Madison', u'United States'),
    (u'Bellingham', u'United States'), (u'Padua', u'Italy'),
    (u'Padova', u'Italy'), (u'Manhattan', u'United States'),
    (u'REMOTE', u'REMOTE'), (u'NO REMOTE', u'DELETE_ME'),
    (u'REMOTE no', u'DELETE_ME'), (u'Poznan', u'Poland'),
    (u'Bellevue, WA', u'United States'), (u'Hillsboro', u'United States'),
    (u'Brighton', u'United Kingdom'), (u'Malibu', u'United States'),
    (u'Somerville', u'United States'), (u'Allahabad', u'India'),
    (u'Hawthorne', u'United States'), (u'Ventura, CA', u'United States'),
    (u'Reading, UK', u'United Kingdom'), (u'Chantilly', u'United States'),
    (u'Dayton', u'United States'), (u'Eindhoven', u'Netherlands'),
    (u'Brooklyn, NY', u'United States')]

for i in extra:
    c = City(i[0], i[1])
    db.session.add(c)

db.session.commit()
db.session.close()

