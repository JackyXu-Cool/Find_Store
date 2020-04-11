from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    jwt_optional
)
from models.store import StoreModel
from models.item import ItemModel
from models.user import UserModel

class Store(Resource):
    @jwt_required
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        else:
            return {"message": "store not found"}, 404

    @jwt_required
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": "store has already exists"}, 400

        user = UserModel.find_by_id(get_jwt_identity())
        store = StoreModel(name, user.id)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurs while inserting the data"}, 500
        
        return store.json(), 201

    @jwt_required
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if not store:
            return {"message": "store does not exist"}

        user = UserModel.find_by_id(get_jwt_identity())
        if store.user.id != user.id:
            return {"message": "You are not allowed to delete this store"}
        
        items = list(filter(lambda x: x.store_id == store.id , ItemModel.find_all()))
        if len(items) != 0:
            return {"message": "Store cannot be deleted when there is still items in it"}

        store.delete_from_db()
        return {"message": "store deleted"} 


class StoreList(Resource):
    def get(self):
        return {"stores": [store.name for store in StoreModel.find_all()]}
    