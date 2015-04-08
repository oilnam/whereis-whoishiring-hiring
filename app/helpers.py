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
        l[pos-1].append(head[1])
    
    return magic(s[1:], l, top, pos)


def mapMonthToName(n):
    m = { 1 : 'January', 2 : 'February', 3 : 'March',
          4 : 'April', 5 : 'May', 6 : 'June',
          7 : 'July', 8 : 'August', 9 : 'September',
          10 : 'October', 11 : 'November', 12 : 'December' }
    try:
        return m[n]
    except:
        return 'Key error'


def lastUpdate():
    if os.getcwd().split('/')[-1] != 'hn-pages':
        os.chdir('build-DB/hn-pages')
    pages = [ os.path.getmtime(f) for f in os.listdir('.') if f.endswith('html') ]

    #return time.gmtime(max(pages))

    return time.strftime("%b %d %Y at %H:%M UTC", time.gmtime(max(pages)))
