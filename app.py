import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister;
from resources.item import Item, ItemList;
from resources.store import Store, StoreList


app = Flask(__name__)

# Connect to postgress database in Heroku OR Connect to local database "data.db"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "00001"    # should be keep secret 
api = Api(app)

jwt = JWT(app, authenticate, identity)  # Create "/auth" endpoint

api.add_resource(Store, "/store/<string:name>")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/<string:name>/items")
api.add_resource(StoreList, "/stores")

api.add_resource(UserRegister, "/register")  # "/register" for storing new users' info into the database 

