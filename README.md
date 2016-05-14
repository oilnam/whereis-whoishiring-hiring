# Where is Who is hiring? hiring?

Overview
--------

This repo contains:
 1. The code for the site http://whereis-whoishiring-hiring.me, under `app`; and
 2. The code to scrape Hacker News' [_Who is hiring?_](https://news.ycombinator.com/user?id=whoishiring) posts and create the database that powers the website, under `database`.
 
You can find a list of FAQ about the project here: http://whereis-whoishiring-hiring.me/faq

Building the database
---------------------

You can either use both Sqlite and MySQL; for the latter, you'll have to stick your password in both `config.py`, `create_everything.sh` and `update_single_item.sh`. Sqlite should just work. (yay!)

#### Create the database from scratch

Clone the repo and install the requirements; then:

    $ cd database
    $ ./create_everything.sh <sqlite | mysql>

#### Update the database with a single HN post

    $ cd database
    $ ./upadte_single_item.sh <hn post id> <sqlite | mysql>

#### Run the tests

    $ cd database
    $ python tests.py
 
Running the web app
-------------------

    $ python run.py

The webapp is trivial enough that no tests are necessary for now.

Contributing
------------
PRs are more than welcome! :) There's a ton of work that could be done, from tidying up the code to implementing new features. I have few ideas but I lack time. If you want to contribute, drop me a line or go ahead and open a PR.

Mandatory boring disclaimer: this stuff is not affiliated with YCombinator, I don't make a single cent for running it etc etc.

Authors
-------
manlio <manlio.poltronieri@gmail.com>

License
-------
Beerware
 





  
  
