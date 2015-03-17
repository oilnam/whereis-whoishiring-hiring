#!flask/bin/python
from app import app, db
import os

app.config.from_object('config.BaseConfiguration')

basedir = os.path.abspath(os.path.dirname(__file__))
if not os.path.exists(os.path.join(basedir, 'app.db')):
    db.create_all()

#app.run()
app.run(host='0.0.0.0')
