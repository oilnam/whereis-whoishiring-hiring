import sys
import os

dir = os.path.join(os.path.dirname(__file__), "../..")
sys.path.append(dir)

from app import db

db.create_all()
