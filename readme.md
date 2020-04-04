# Find_Store

This is a REST API developed with Flask, Flask-RESTful, and Flask-SQLAlchemy.
<br />
It is now deployed on Heroku: https://find-stores-api.herokuapp.com/


## Endpoints
* /stores   
    * GET  get a list of current existing stores
* /store/<string:name>
    * GET  get the store information with name=<name>
    * POST  post the store information to the database with name=<name>
    * DELETE  delete the store with name=<name> (It cannoe be reached if there is still items in it)
