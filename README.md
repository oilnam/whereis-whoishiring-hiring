# Where is Who is hiring? hiring?

This repo contains:
 1. The source code to the site http://whereis-whoishiring-hiring.me (Flask codebase)
 2. The scripts to scrape Hacker News' "Who is hiring?" posts and create the database behind the website.
 
You can find a list of FAQ about the website here: http://whereis-whoishiring-hiring.me/faq

A complete (Sqlite) copy of the database is available for download [here](https://www.dropbox.com/s/farbls5hbkhbc1i/last.db.zip?dl=0); however, if you'd rather build your own copy from scratch (maybe you want to twist it a bit?), this is how you do it:

Building the database
---------------------
Everything needed to build the db can be found in `build-DB`. It is easy to single out these scripts from the website and use them as a stand-alone app. Anyway, to build the whole thing:

    $ git clone https://github.com/oilnam/whereis-whoishiring-hiring.git
    $ cd whereis-whoishiring-hiring
    $ pip install -r requirements
    $ cd build-DB
    $ ./build_db.sh <sqlite> or <mysql>

The main building script `build_db.sh` is pretty self explanatory; anyhow, this is what you might want to know:

 - you can either use Sqlite or MySQL; if you go for the latter, you have to fill in db name/user/passwd at the top of the script.
 - you have to comment/uncomment the `download_pages` function to wget a copy of the "Who is hiring?" pages from HN, as well as a list of cities from Wikipedia. Usually, you want to download them the first time and then comment the line out.
 
`build_db.sh` is a wrapper that runs the following:

 - `importWiki.py` gets a list of cities from [Wikipedia](http://en.wikipedia.org/wiki/List_of_cities_by_longitude), plus many more hand-picked by me.
 - `importHN.py` processes all "Who is hiring?" pages found in `hn-pages`. 
 - `refine_db.sql` contains a bunch of SQL queries used to refine the db.

It also *drops* all the tables every time you run it. To give some reference, building the db from scratch takes less then half a minute on my MacbookPro. 

Authors
-------
manlio <manlio.poltronieri@gmail.com>

License
-------
Beerware
 





  
  
