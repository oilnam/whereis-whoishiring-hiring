from bs4 import BeautifulSoup as bs
import os
import re
import requests
import sys
from time import sleep

dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(dir)
from app import db
from app.models import City, Job


def get_whoishiring_submissions():
    print('Querying who is hiring ? submissions...')
    url = 'https://hn.algolia.com/api/v1/search_by_date?query=hiring&tags=story,%28author__whoishiring,%20author_whoishiring%29'
    page = 0
    thread_ids = []
    while True:
        r = requests.get('{0}&page={1}'.format(url, page))
        json = r.json()
        if json['hits']:
            for thread in json['hits']:
                thread_ids.append(thread['objectID'])
            sleep(1)
            page += 1
        else:
            break
    return thread_ids


def process_page(page_id, update=False, localPage=None):
    print('processing page {}'.format(page_id))
    if localPage:
        page = open(localPage, 'r')
        s = bs(page)
    else:
        r = requests.get('https://news.ycombinator.com/item?id={}'.format(page_id))
        s = bs(r.text)
    try:
        month, year = extract_month_and_year(s)
        if update:
            delete_jobs(month, year)
        jobs = extract_jobs_from_page(s)
        save_city_given_list_of_posts(jobs, month, year)
    except ValueError:
        print('skipping {}'.format(page_id))
        return # not a monthly who is hiring thread, skip it


def delete_jobs(month, year):
    print('deleting jobs for {0} {1}'.format(month, year))
    jobs = Job.query.filter(Job.month == month).filter(Job.year == year).all()
    for j in jobs:
        db.session.delete(j)


def extract_month_and_year(s):
    t = s.title.get_text()
    title = t[t.index('(')+1:t.index(')')].split(' ')
    month = month_to_number(title[0][:3])
    return (month, title[1])


def month_to_number(month):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return months.index(month) + 1


def extract_jobs_from_page(s):
    extracted_jobs_and_hn_ids = []
    posts = s.find('table').findAll('tr')[3].findAll('table')[1].findAll('tr', recursive=False)
    for post in posts:
        content = post.find('tr')
        # check the post is not a reply
        if content.find(lambda tag : tag.name == 'img' and int(tag['width']) == 0):
            plain_text = content.find('span', class_ = 'comment').get_text()
            try:
                hn_id = content.findAll('a')[2]['href'].split('=')[1]
                extracted_jobs_and_hn_ids.append((content, plain_text, hn_id))
            except IndexError:
                continue # the post has been removed, skip it
    return extracted_jobs_and_hn_ids


def save_city_given_list_of_posts(posts, month, year):
    all_cities = { city : id for (city, id) in db.session.query(City.name, City.id).all() }
    unmatched_jobs = []
    # posts is a list of tuples (html_post, plain_post, hackernews_hd)
    for post in posts:
        at_least_one_match = False
        (html_post, plain_post, hn_id) = post
        for city in all_cities:
            maybe_city = plain_post.find(city)
            if maybe_city != -1:
                if re.match(city + '([^a-z]|$)', plain_post[maybe_city:]):
                    newJob = Job(unicode(html_post), month, year, hn_id, all_cities[city])
                    db.session.add(newJob)
                    at_least_one_match = True
        if not at_least_one_match:
            unmatched_jobs.append((plain_post, hn_id))
    db.session.commit()
    db.session.close()

    with open('debug/no_matches-{0}-{1}.txt'.format(month, year), 'w') as f:
        for (job, hn_id) in unmatched_jobs:
            f.write(hn_id)
            f.write(job.encode('utf-8'))


def main():
    ids = get_whoishiring_submissions()
    for submission in ids:
        process_page(submission)

if __name__== "__main__":
    main()

