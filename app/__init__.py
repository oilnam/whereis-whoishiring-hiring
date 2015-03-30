from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config.from_object('config.BaseConfiguration')
db = SQLAlchemy(app)

toolbar = DebugToolbarExtension(app)

from app import views, models
