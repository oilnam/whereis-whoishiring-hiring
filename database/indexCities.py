import os
import sys
import unicodecsv as csv

dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(dir)

from app import db
from app.models import City, Job, Europe, soCal, noCal, SEAsia

with open('resources/all_cities.csv', 'r') as f:
	reader = csv.reader(f)
	for row in reader:
		city = City(row[0], row[1])
		db.session.add(city)
	db.session.commit()


with open('resources/europe.csv', 'r') as f:
	reader = csv.reader(f)
	for row in reader:
		c = Europe(row[0])
		db.session.add(c)
	db.session.commit()

with open('resources/no_cal.csv', 'r') as f:
	reader = csv.reader(f)
	for row in reader:
		c = noCal(row[0])
		db.session.add(c)
	db.session.commit()


with open('resources/so_cal.csv', 'r') as f:
	reader = csv.reader(f)
	for row in reader:
		c = soCal(row[0])
		db.session.add(c)
	db.session.commit()


with open('resources/seasia.csv', 'r') as f:
	reader = csv.reader(f)
	for row in reader:
		c = SEAsia(row[0])
		db.session.add(c)
	db.session.commit()


remote = [('REMOTE', 'REMOTE'), ('NO REMOTE', '_remote_'),
          ('REMOTE no', '_remote_'), ('Remote', '_remote_'),
          ('Remote not', '_remote_'), ('No Remote', '_remote_')]

for i in remote:
    c = City(unicode(i[0]), unicode(i[1]))
    db.session.add(c)
db.session.commit()


db.session.close()

