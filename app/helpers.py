import bisect
from datetime import date
import time
import os

def magic(s, l = [], top = 0, pos = 0):
    if len(s) == 0:
        return l

    head = s[0]
    if head[0] != top:
        l.append([head[0], head[1]])
        top = head[0]
        pos += 1
    else:
        bisect.insort(l[pos-1], head[1])

    return magic(s[1:], l, top, pos)


def month_to_name(n):
    m = { 1 : 'January', 2 : 'February', 3 : 'March',
          4 : 'April', 5 : 'May', 6 : 'June',
          7 : 'July', 8 : 'August', 9 : 'September',
          10 : 'October', 11 : 'November', 12 : 'December' }
    try:
        return m[n]
    except:
        return 'Key error'


def last_db_update():
    try:
        t = os.path.getmtime('database/last_update')
        return time.strftime("%b %d %Y at %H:%M UTC", time.gmtime(t))
    except OSError:
        return 'unknown'


def get_frontpage_month_and_year():
    """ get the month and year to be displayed in the front page from
        a local file that looks like: 'month-year', e.g. 5-2016
    """
    try:
        with open('frontpage_month_and_year.txt', 'r') as f:
            (month, year) = f.readline().strip('\n').split('-')
            return month, year
    except (IOError, AttributeError):
        return date.today().month, date.today().year

