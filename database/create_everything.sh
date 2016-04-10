#!/bin/bash

rm -f ../app.db

python init_db.py
python index_cities.py
python full_hn_reindex.py
sqlite3 ../app.db < refine_db.sql

