from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from security import authenticate, identity
from item import ItemList, Item
from user import UserRegister

# resources are usually mapped with databases

app = Flask(__name__)
api = Api(app)
app.secret_key = "ram"

jwt = JWT(app, authenticate, identity)  # /auth


api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')

if __name__ == "__main__":
    app.run(port=5000, debug=True)