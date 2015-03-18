#!/bin/bash

function download_pages {
    # 2015
    wget https://news.ycombinator.com/item?id=8822808 -O 1-2015.html
    wget https://news.ycombinator.com/item?id=8980047 -O 2-2015.html
    wget https://news.ycombinator.com/item?id=9127232 -O 3-2015.html

    #2014
    wget https://news.ycombinator.com/item?id=6995020 -O 1-2014.html
    wget https://news.ycombinator.com/item?id=7162197 -O 2-2014.html
    wget https://news.ycombinator.com/item?id=7324236 -O 3-2014.html
    wget https://news.ycombinator.com/item?id=7507765 -O 4-2014.html
    wget https://news.ycombinator.com/item?id=7679431 -O 5-2014.html
    wget https://news.ycombinator.com/item?id=7829042 -O 6-2014.html
    wget https://news.ycombinator.com/item?id=7970366 -O 7-2014.html
    wget https://news.ycombinator.com/item?id=8120070 -O 8-2014.html
    wget https://news.ycombinator.com/item?id=8252715 -O 9-2014.html
    wget https://news.ycombinator.com/item?id=8394339 -O 10-2014.html
    wget https://news.ycombinator.com/item?id=8542892 -O 11-2014.html
    wget https://news.ycombinator.com/item?id=8681040 -O 12-2014.html

    mkdir -p hn-pages
    mv *.html hn-pages

    # Wikipedia
    wget http://en.wikipedia.org/wiki/List_of_cities_by_longitude -O wiki.html
}

# comment out the following line after the first download
#download_pages

# build the db
echo "Building the db; this will take a little while..."
rm -f database-full.db
rm -f ../app.db

python createDB.py
python importWiki.py
python importHN.py

sqlite3 ../app.db < refine_db.sql
cp ../app.db database-full.db

python ../tests.py
