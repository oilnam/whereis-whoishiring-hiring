#!/bin/bash

MYSQL_DB="whoishiring"
MYSQL_USR="whoishiring"
MYSQL_PWD=""

USAGE() {
    echo "Usage: ./update_single_item.sh <hn post id> <sqlite | mysql>"
}

if [ $# -ne "2" ]; then
    USAGE
    exit 1
fi

python src/single_hn_reindex.py $1

if [ $2 = "sqlite" ]; then
    sqlite3 ../app.db < src/refine_db.sql
fi

if [ $2 = "mysql" ]; then
    mysql $MYSQL_DB -u $MYSQL_USR --password=$MYSQL_PWD < src/refine_db.sql
fi

touch last_update
