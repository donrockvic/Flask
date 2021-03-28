from flask import Flask, request
from flask_jwt import JWT, jwt_required
from flask_restful import Resource, Api, reqparse

from security import authenticate, identity

# resources are usually mapped with databases

app = Flask(__name__)
api = Api(app)
app.secret_key = "ram"

jwt = JWT(app, authenticate, identity)  # /auth

Items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        help="This field can't be blank",
        required=True
    )

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, Items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, Items), None):
            return {"message": "An item with name {} already exists".format(name)}, 400
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        Items.append(item)
        return item, 201

    def delete(self, name):
        global Items
        Items = list(filter(lambda x: x['name'] != name, Items) )
        return {'message': 'Item Deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, Items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            Items.append(item)
        else:
            item.update(data)
        return item


class ItemList(Resource):
    def get(self):
        return {'items': Items}


api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')

app.run(port=5000, debug=True)