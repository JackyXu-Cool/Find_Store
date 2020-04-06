from flask_restful import Resource, reqparse
from models.store import StoreModel
from models.item import ItemModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        else:
            return {"message": "store not found"}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": "store has already exists"}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurs while inserting the data"}, 500
        
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if not store:
            return {"message": "store does not exist"}

        items = list(filter(lambda x: x.store_id == store.id , ItemModel.find_all()))
        if len(items) != 0:
            return {"message": "Store cannot be deleted when there is still items in it"}

        store.delete_from_db()
        return {"message": "store deleted"} 


class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.find_all()]}
    