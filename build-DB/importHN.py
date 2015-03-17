from bs4 import BeautifulSoup as bs
import re
import sys
import os

# this a bit hackeryish. Should I rewrite everything in plain SQL?
dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(dir)
from app import db
from app.models import City, Job

def importComments(_fileList, _month, _year):

    dd = { city : id for (city, id) in db.session.query(City.name, City.id).all() }

    s = bs(open(_fileList))
    comments = s.find_all('span', class_ = 'comment')

    with open('hn-pages/debug-{0}-{1}.txt'.format(_month, _year), 'w') as f:
        for c in comments:
            plain = c.get_text()
            found_flag = False
            for city in dd:
                position = plain.find(city)
                if position != -1:
                    found_flag = True
                    if re.match(city + '([^a-z]|$)', plain[position:]):
                        newJob = Job(unicode(c), _month, _year, dd[city])
                        db.session.add(newJob)
                    else:
                        f.write('--DITCHED BY REGEX--\n')
                        f.write(plain[position:position+50].encode('utf-8'))
                        f.write('\n\n\n')
            if not found_flag:
                f.write('--NO CITY FOUND FOR--\n')
                f.write(plain.encode('utf-8'))
                f.write('\n\n\n')

        f.write('Imported successfully!')
        db.session.commit()
        db.session.close()


importComments('hn-pages/3-15.html', 3, 2015)
importComments('hn-pages/2-15.html', 2, 2015)
importComments('hn-pages/1-15.html', 1, 2015)
importComments('hn-pages/12-14.html', 12, 2014)
importComments('hn-pages/11-14.html', 11, 2014)



