import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    jwt_refresh_token_required, 
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)
from models.user import UserModel
from blacklist import BLACKLIST

class UserRegister(Resource):



    parser = reqparse.RequestParser()
    parser.add_argument("username", 
        type=str,
        required=True,
        help="This field cannot be left blank"
    )

    parser.add_argument("password", 
        type=str,
        required=True,
        help="This field cannot be left blank"
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        
        if UserModel.find_by_username(data["username"]):
            return {"message": "username has already exists"}, 400

        user = UserModel(data["username"], data["password"])
        user.save_to_db()

        return {"message": "new user '{}' is created".format(data["username"])}, 201

class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404

        for store in user.stores:
            store.delete_from_db()

        user.delete_from_db()
        return {"message": "user has been deletes"}, 200

class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", 
        type=str,
        required=True,
        help="This field cannot be left blank"
    )

    parser.add_argument("password", 
        type=str,
        required=True,
        help="This field cannot be left blank"
    )

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()

        user = UserModel.find_by_username(data["username"])

        if user and data["password"] == user.password:
            access_token = create_access_token(identity=user.id, fresh=True)  # Token is from "Login"
            refresh_token = create_refresh_token(identity=user.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 200
        
        return {"message": "Invalid credentials"}, 401
    
class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {
            "message": "User log out!"
        }
