import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        help="This field can't be blank",
        required=True
    )
    parser.add_argument(
        'password',
        type=str,
        help="This field can't be blank",
        required=True
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        username = data["username"]
        if UserModel.find_by_username(username):
            return {"message": "user with given username already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()
        return {"message": "user created successfully"}, 201
