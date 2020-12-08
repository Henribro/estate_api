# How to run and test the API

## Install dependencies

In the **api** directory run :

    $ pip install -r requirements.txt

## Start server

In the **api** directory run :

    $ python main.py

The server runs on http://127.0.0.1:5000/

## Fill the database

In the **api** directory run :

    $ python db_setup.py

It will fill the database with some users, some houses and some rooms

## Test

Go on an internet browser

#Estate browsing

Try 
	http://127.0.0.1:5000/browse/Caen
	http://127.0.0.1:5000/browse/Magne
	http://127.0.0.1:5000/browse/Marseille

#User access

Try
	http://127.0.0.1:5000/user/0
	http://127.0.0.1:5000/user/1
