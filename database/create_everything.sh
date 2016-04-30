#!/bin/bash

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

CREATE() {
    python tests.py
    python init_db.py
    python index_cities.py
    python full_hn_reindex.py
}


if [ $1 = "sqlite" ]; then
    rm -f ../app.db
    CREATE
    sqlite3 ../app.db < refine_db.sql
fi

if [ $1 = "mysql" ]; then
    mysql $MYSQL_DB -u $MYSQL_USR --password=$MYSQL_PWD -e "DROP TABLE job;"
    mysql $MYSQL_DB -u $MYSQL_USR --password=$MYSQL_PWD -e "DROP TABLE city;"
    CREATE
    mysql $MYSQL_DB -u $MYSQL_USR --password=$MYSQL_PWD < refine_db.sql

# touch a file to get last update time
touch last_update
