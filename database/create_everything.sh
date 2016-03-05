#!/bin/bash

rm -f ../app.db

python createDB.py
python indexCities.py
sqlite3 ../app.db < refine_db.sql
