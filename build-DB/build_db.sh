#!/bin/bash

# replace these with your own variables
MYSQL_DB="whoishiring"
MYSQL_USR="whoishiring"
MYSQL_PWD=""


USAGE() {
    echo "Usage: ./build_db.sh <sqlite> or <mysql>"
}

if [ $# -ne "1" ]; then
    USAGE
    exit 1
fi

download_pages () {
    # 2015
    wget https://news.ycombinator.com/item?id=8822808 -O 2015-1.html
    wget https://news.ycombinator.com/item?id=8980047 -O 2015-2.html
    wget https://news.ycombinator.com/item?id=9127232 -O 2015-3.html
    wget https://news.ycombinator.com/item?id=9303396 -O 2015-4.html

    #2014
    wget https://news.ycombinator.com/item?id=6995020 -O 2014-1.html
    wget https://news.ycombinator.com/item?id=7162197 -O 2014-2.html
    wget https://news.ycombinator.com/item?id=7324236 -O 2014-3.html
    wget https://news.ycombinator.com/item?id=7507765 -O 2014-4.html
    wget https://news.ycombinator.com/item?id=7679431 -O 2014-5.html
    wget https://news.ycombinator.com/item?id=7829042 -O 2014-6.html
    wget https://news.ycombinator.com/item?id=7970366 -O 2014-7.html
    wget https://news.ycombinator.com/item?id=8120070 -O 2014-8.html
    wget https://news.ycombinator.com/item?id=8252715 -O 2014-9.html
    wget https://news.ycombinator.com/item?id=8394339 -O 2014-10.html
    wget https://news.ycombinator.com/item?id=8542892 -O 2014-11.html
    wget https://news.ycombinator.com/item?id=8681040 -O 2014-12.html

    mkdir -p hn-pages
    mv *.html hn-pages

    # Wikipedia
    wget http://en.wikipedia.org/wiki/List_of_cities_by_longitude -O wiki.html
}

# comment out the following line after the first download
# download_pages

# build the db
echo
echo "Building the db; this will take a little while..."
echo

if [ $1 = "sqlite" ]; then
    echo "Using db sqlite"
    # delete old db
    rm -f database-full.db
    rm -f ../app.db

    # create and import stuff
    echo "Importing cities and jobs..."
    python createDB.py
    python importWiki.py
    python importHN.py

    echo "Cleaning up..."
    # cleanup
    sqlite3 ../app.db < refine_db.sql
    cp ../app.db database-full.db
fi


if [ $1 = "mysql" ]; then
    echo "Using db mysql"
    # drop tables
    mysql $MYSQL_DB -u $MYSQL_USR --password=$MYSQL_PWD -e "DROP TABLE job;"
    mysql $MYSQL_DB -u $MYSQL_USR --password=$MYSQL_PWD -e "DROP TABLE city;"

    # create and import stuff
    echo "Importing cities and jobs..."
    python createDB.py
    python importWiki.py
    python importHN.py
    
    # cleanup
    echo "Cleaning up..."
    mysql $MYSQL_DB -u $MYSQL_USR --password=$MYSQL_PWD < refine_db.sql
fi


# run tests
python ../tests.py
