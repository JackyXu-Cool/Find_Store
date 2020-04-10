import os

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import UserRegister, User, UserLogin, UserLogout
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from blacklist import BLACKLIST

app = Flask(__name__)

# Connect to postgress database in Heroku OR Connect to local database "data.db"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = "00001"   
api = Api(app)

jwt = JWTManager(app)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST  

api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/<string:store_name>/items")
api.add_resource(User, "/user/<int:user_id>")

api.add_resource(UserRegister, "/register") 
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
