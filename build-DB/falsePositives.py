import sys
import os
from sqlalchemy import func

dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(dir)
from app import db
from app.models import City, Job

# the idea here is that if a post is very short (<200 chars) and
# doesn't contain any link, it probably isn't a job offer.

suspects = db.session.query(Job.id, Job.description, 
                            func.length(Job.description).label('llen')).\
                            filter('llen < 200').\
                            order_by('llen')

with open('possible-false-positives.txt', 'w') as f:
    for s in suspects:
        ss = s[1].strip('<span class="comment"><font color="#000000">')
        ss = ss.strip('</font></span>')
        if ss.find('<a href=') == -1:
            f.write('{0}\n{1}\n\n\n'.format(s[0], ss.encode('utf-8')))
    
    f.write('All IDs in a handy set:\n\n')
    for s in suspects:
        f.write('{0}, '.format(s[0]))
