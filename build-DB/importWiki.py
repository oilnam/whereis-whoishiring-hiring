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
    ('Mountain View', 'United States'), ('San Mateo', 'United States'),
    ('Santa Monica', 'United States'), ('Santa Clara', 'United States'),
    ('Cupertino', 'United States'), ('Palo Alto', 'United States'),
    ('Camarillo', 'United States'), ('Los Altos', 'United States'),
    ('Redwood', 'United States'), ('Sunnyvale', 'United States'),
    ('Emeryville', 'United States'), ('Orange County', 'United States'),
    ('Oakland', 'United States'), ('Paoli, PA', 'United States'),
    ('Mexico City', 'Mexico'), ('Buenos Aires', 'Argentina'),
    ('Hong Kong', 'HK'), ('Leuven', 'Belgium'),
    ('Mumbai', 'India'), ('Berkeley', 'United States'),
    ('Delhi', 'India'), ('Waltham', 'United States'),
    ('Naperville', 'United States'), ('Harbor Springs', 'United States'),
    ('Irvine', 'United States'), ('Durham', 'United States'),
    ('Chattanooga', 'United States'), ('Redmond', 'United States'),
    ('New York', 'United States'), ('San Jose', 'United States'),
    ('NYC', 'United States'), ('SF', 'United States'),
    ('LA, CA', 'United States'), ('Bloomington', 'United States'),
    ('Cambridge', 'United States'), ('Cambridge, UK', 'United Kingdom'),
    ('Zurich', 'Switzerland'), ('Nice, France', 'France'),
    ('Versailles', 'France'), ('Iron Mountain', 'United States'),
    ('Lincoln, NE', 'United States'), ('Windsor, ON', 'United States'),
    ('Mobile, AL', 'United States'), ('Pierre, SD', 'United States'),
    ('Trento', 'Italy'), ('Taghazout', 'Morocco'),
    ('Pasadena', 'United States'), ('Menlo Park', 'United States'),
    ('West Hollywood', 'United States'), ('Chennai', 'India'),
    ('Myrtle Beach', 'United States'), ('Gurgaon', 'India'),
    ('Culver City', 'United States'), ('Frederick, MD', 'United States'),
    ('Fort Worth', 'United States'), ('Goettingen', 'Germany'),
    ('Los Gatos', 'United States'), ('Florianopolis', 'Brazil'),
    ('Boca Raton', 'United States'), ('Aliso Viejo', 'United States'),
    ('Ann Arbor', 'United States'), ('Newark', 'United States'),
    ('New Haven', 'United States'), ('Madison', 'United States'),
    ('Bellingham', 'United States'), ('Padua', 'Italy'),
    ('Padova', 'Italy'), ('Manhattan', 'United States'),
    ('REMOTE', 'REMOTE'), ('NO REMOTE', 'DELETE_ME'),
    ('REMOTE no', 'DELETE_ME'), ('Poznan', 'Poland'),
    ('Bellevue, WA', 'United States'), ('Hillsboro', 'United States'),
    ('Brighton', 'United Kingdom'), ('Malibu', 'United States'),
    ('Somerville', 'United States'), ('Allahabad', 'India'),
    ('Hawthorne', 'United States'), ('Ventura, CA', 'United States'),
    ('Reading, UK', 'United Kingdom'), ('Chantilly', 'United States'),
    ('Dayton', 'United States'), ('Eindhoven', 'Netherlands'),
    ('Brooklyn, NY', 'United States'), ('Rockford', 'United States'),
    ('Newton', 'United States'), ('Burbank', 'United States'),
    ('St Paul', 'United States'), ('Saint Paul', 'United States'),
    ('Burlingame', 'United States'), ('Conshohocken', 'United States'),
    ('Cary, NC', 'United States'), ('Troy, NC', 'United States'),
    ('Palm Beach', 'United States'), ('Campbell', 'United States'),
    ('Milano', 'Italy'), ('Herndon', 'United States'),
    ('Foster City', 'United States'), ('LONDON', 'United Kingdom'),
    ('SAN FRANCISCO', 'United States'), ('NEW YORK', 'United States'),
    ('SEATTLE', 'United States'), ('El Segundo', 'United States'),
    ('New Hope', 'United States'), ('Littleton', 'United States')]

for i in extra:
    c = City(unicode(i[0]), unicode(i[1]))
    db.session.add(c)

db.session.commit()
db.session.close()

