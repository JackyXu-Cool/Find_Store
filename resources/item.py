from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims, 
    jwt_optional, 
    get_jwt_identity, 
    fresh_jwt_required
)
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
        type=float,
        required=True,
        help="Cannot be left blank!")
    parser.add_argument("store_id",
        type=int,
        required=True,
        help="Every item needs a store id!")

    @jwt_required
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)
        except:
            return {"message": "an error occur"}, 500

        if item:
            return item.json()
        else:
            return {"message": "'{}' does not exist".format(name)}, 404

    @fresh_jwt_required
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "That item has already exists"}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, data["price"], data["store_id"])

        try:
            item.save_to_db()
        except:
            return {"message": "an error occur"}, 500 # Server error

        return item.json(), 201

    @jwt_required
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": "item deleted"}
        return {"message": "item not found"}

    @fresh_jwt_required
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data["price"], data["store_id"])
        else:
            item.price = data["price"]
            item.store_id = data["store_id"]

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    @jwt_optional
    def get(self, store_name):
        user_id = get_jwt_identity()
        items = filter(lambda x: x.store.name == store_name, ItemModel.find_all())

        if user_id:
            return {"items": [item.json() for item in items]}
        else:
            return {
                "items": [item.name for item in items],
                "message": "More data available if you log in"
            }



