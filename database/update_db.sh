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


# build the db
echo
echo "Building the db; this will take a little while..."
echo

if [ $1 = "sqlite" ]; then
    echo "Using db sqlite"
    python updateDB.py
    echo "Cleaning up..."
    # cleanup
    sqlite3 ../app.db < refine_db.sql
    cp ../app.db database-full.db
fi


if [ $1 = "mysql" ]; then
    echo "Using db mysql"
    # create and import stuff
    python updateDB.py
    
    # cleanup
    echo "Cleaning up..."
    mysql $MYSQL_DB -u $MYSQL_USR --password=$MYSQL_PWD < refine_db.sql
fi


# run tests
python ../tests.py

# touch a file to get last update time
touch last_update
