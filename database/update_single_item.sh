#!/bin/bash

USAGE() {
    echo "Usage: ./update_single_item.sh <hn post id>"
}

if [ $# -ne "1" ]; then
    USAGE
    exit 1
fi

python single_hn_reindex.py $1
sqlite3 ../app.db < refine_db.sql

