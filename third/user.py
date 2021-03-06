import sqlite3
from flask_restful import Resource, reqparse


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users where username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            # user = cls(row(0), row(1), row(2))
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users where id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            # user = cls(row(0), row(1), row(2))
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user


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
        if User.find_by_username(username):
            return {"message": "user with given username already exists"}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        insert_query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(insert_query, (data['username'], data['password'],))

        connection.commit()
        connection.close()
        return {"message": "user created successfully"}, 201
