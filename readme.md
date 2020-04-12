# Find_Store

This is a REST API developed with Flask, Flask-RESTful, FLask-JWT-Extended and Flask-SQLAlchemy.
<br />
It is now deployed on Heroku: https://find-stores-api.herokuapp.com/

## Overview
An unanthenticated user can do the following:
<ol>
<li> Get all the store name.</li>
<li> Get the names of every item in one store</li>
</ol>
<br />
An anthenticated user can do the following:
<ol>
<li> Create/delete/access one's own store </li>
<li> Create/update/delete/access an item in one's own store </li>
<li> Get the information of all items in one's own store </li>
</ol>

## All Endpoints
* /register
    * POST register a new users {username, password}
* /login
    * POST Login {username, password}
* /logout
    * POST logout
* /stores   
    * GET  get a list of current existing stores
* /store/string:name
    * GET  get the store information
    * POST  create a new store  
    * DELETE  delete a store  
* /string:name/items
    * GET  a list of items inside the specific store  
* /item/string:name
    * GET  get an item information
    * POST  create an new item  
    * PUT  update the existing item  
    * DELETE  delete an item  
    * **Input format**: {float:price, string:store_name}
* /user/int:user_id
    * GET  access an user by its id
    * Delete  delete an user

## Sample JSON Format
### User
```
{  
    "id": 1, 
    "username": "Jacky",
    "stores": [
        "Burgers","McDonalds
        ]
}
```
### Store
```
{
    "id": 1,
    "name": "Burgers",
    "items": [
        {
            "id": 1,
            "name": "chicken",
            "price": 2.35
        }
    ],
    "owner": "Tim"
}
```
### Item
```
{
    "id": 1,
    "name": "chicken",
    "price": 2.35
}
```
