from bs4 import BeautifulSoup as bs
import re
import sys
import os
from string import capwords

# this a bit hackeryish. Should I rewrite everything in plain SQL?
dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(dir)
from app import db
from app.models import City, Job


def monthify(s):
    m = { u'January':1, u'February':2, u'March':3, u'April':4,
          u'May':5, u'June':6, u'July':7, u'August':8,
          u'September':9, u'October':10, u'November':11, u'December':12}
    return m[capwords(s)]


def importComments(_fileList):

    # load all cities in a dict for faster lookup
    dd = { city : id for (city, id) in db.session.query(City.name, City.id).all() }

    s = bs(open(os.path.join('hn-pages', _fileList)))
    t = s.title.get_text()
    title = t[t.index('(')+1:t.index(')')].split(' ')
    month = monthify(title[0])
    year = title[1]

    # let's dig through this thing
    hnmain = s.find('table')
    outerTable = hnmain.findAll('tr')[3]
    innerTable = outerTable.findAll('table')[1]

    # inside innerTable, every <tr> is a post,
    # but the actual stuff in nested in yet another <tr> (wtf?)
    posts = innerTable.findAll('tr', recursive=False)

    with open('hn-pages/debug-{0}-{1}.txt'.format(year, month), 'w') as f:
        for p in posts:
            c = p.find('tr')
            # if the post is not a reply, process it
            if c.find(lambda tag : tag.name == 'img' and int(tag['width']) == 0):
                content = c.find('span', class_ = 'comment')
                plain = content.get_text()
                found_flag = False
                for city in dd:
                    position = plain.find(city)
                    if position != -1:
                        found_flag = True
                        if re.match(city + '([^a-z]|$)', plain[position:]):
                            # get the original HN id and push the new job
                            hn_id = c.findAll('a')[2]['href'].split('=')[1]
                            newJob = Job(unicode(content), month, year, hn_id, dd[city])
                            db.session.add(newJob)
                        else:
                            f.write('--DITCHED BY REGEX--\n')
                            f.write(plain[position:position+50].encode('utf-8'))
                            f.write('\n\n\n')
                if not found_flag:
                    f.write('--NO CITY FOUND FOR--\n')
                    f.write(plain.encode('utf-8'))
                    f.write('\n\n\n')
        # end of for p in posts
        f.write('Imported successfully!')
        db.session.commit()
        db.session.close()


def main():

    for f in os.listdir('hn-pages'):
        if f.endswith('.html'): 
            print 'processing ' + str(f)
            importComments(f)


if __name__== "__main__":
    main()

