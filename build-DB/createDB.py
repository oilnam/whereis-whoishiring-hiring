import sys
import os

# this is a bit hackeryish. Should I rewrite everything in plain SQL?
dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(dir)

from app import db

db.create_all()
