from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
from models.store import StoreModel

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

    @jwt_required()
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)
        except:
            return {"message": "an error occur"}, 500

        if item:
            return item.json()
        else:
            return {"message": "'{}' does not exist".format(name)}, 404

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

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
           item.delete_from_db()
        
        return {"message": "item deleted"}

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
    def get(self, store_name):
        store = StoreModel.find_by_name(store_name)

        items = filter(lambda x: x.store_id == store.id, ItemModel.find_all())

        return {"items": [item.json() for item in items]}



