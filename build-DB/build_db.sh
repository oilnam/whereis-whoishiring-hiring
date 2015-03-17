#!/bin/bash

rm -f database-full.db
rm -f ../app.db

python createDB.py
python importWiki.py
python importHN.py

sqlite3 ../app.db < refine_db.sql
cp ../app.db database-full.db

python ../tests.py
