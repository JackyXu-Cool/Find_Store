from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims, 
    jwt_optional, 
    get_jwt_identity, 
    fresh_jwt_required
)
from models.item import ItemModel
from models.store import StoreModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
        type=float,
        required=True,
        help="Cannot be left blank!")
    parser.add_argument("store_name",
        type=str,
        required=True,
        help="You must enter the store name you want to store this item in!")

    @jwt_required
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)
        except:
            return {"message": "an error occur"}, 500

        if item:
            user_id = get_jwt_identity()
            if user_id != item.store.user_id:
                return {"message": "You can only access the item in your own store"}
            return item.json()
        else:
            return {"message": "'{}' does not exist".format(name)}, 404

    @fresh_jwt_required
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "That item has already exists"}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, data["price"], data["store_name"])

        user_id = get_jwt_identity()
        if user_id != StoreModel.find_by_id(item.store_id).user_id:
            return {"message": "You can only create new item in your own store"}

        try:
            item.save_to_db()
        except:
            return {"message": "an error occur"}, 500 # Server error

        return item.json(), 201

    @jwt_required
    def delete(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            user_id = get_jwt_identity()
            if user_id != StoreModel.find_by_id(item.store_id).user_id:
                return {"message": "You can only delete item in your own store"}
            item.delete_from_db()
            return {"message": "item deleted"}

        return {"message": "item not found"}

    @fresh_jwt_required
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data["price"], data["store_name"])
        else:
            item.price = data["price"]
            item.store_name = data["store_name"]

        user_id = get_jwt_identity()
        if user_id != StoreModel.find_by_id(item.store_id).user_id:
            return {"message": "You can only update item in your own store"}

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    @jwt_optional
    def get(self, store_name):
        user_id = get_jwt_identity()
        items = filter(lambda x: x.store.name == store_name, ItemModel.find_all())

        if user_id == StoreModel.find_by_name(store_name).user_id:
            return {"items": [item.json() for item in items]}
        else:
            if not user_id:
                return {
                    "items": [item.name for item in items],
                    "message": "More data available if you log in"
                }
            else:
                return {
                    "items": [item.name for item in items],
                    "message": "You can only get full information of the items in your own store"
                }



