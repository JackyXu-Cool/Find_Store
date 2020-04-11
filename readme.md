# Find_Store

This is a REST API developed with Flask, Flask-RESTful, FLask-JWT-Extended and Flask-SQLAlchemy.
<br />
It is now deployed on Heroku: https://find-stores-api.herokuapp.com/

## Overview
An unanthenticated user can do the following:
1. Get all the store name.
2. Get the names of every item in one store
<br />
An anthenticated user can do the following:
1. Create/update/delete a store, and get access to all the information to one's own store
2. Create/update/delete an item in one's store
3. Get the information of all items in one's own store

## All Endpoints
* /register
    * POST register a new users (username, password needed)
* /login
    * POST Login (username, password needed)
* /logout
    * POST logout
* /stores   
    * GET  get a list of current existing stores
* /store/string:name
    * GET  get the store information
    * POST  post the store information to the database
    * DELETE  delete the store with (It cannot be reached if there is still items in it)
* /string:name/items
    * GET  a list of items inside the specific store

## JSON Format
