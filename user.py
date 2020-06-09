import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel
from security import hashPassword
from os import urandom
import base64
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
class UserSearch(Resource):

    # returns list of users matching 'username' argument
    @jwt_required
    def get(self, username):
        if len(username) < 4:
            return {"message": "Username is too short"}, 400
        users = UserModel.find_many_by_username(username)

        return {
            'users': [user.json() for user in users]
        }


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "password", type=str, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "about", type=str, required=False
    )
    @classmethod
    def post(cls):
        data = cls.parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {"message": "User already exists"}, 400

        password = data["password"]
        salt = urandom(32)
        data["password"] = hashPassword(password, salt)
        # encoding random salt bytes to b64 format(db write)
        data["salt"] = base64.b64encode(salt)
        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'User created successfully.'}, 201

class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "password", type=str, required=True, help="This field cannot be left blank!"
    )
    
    @classmethod
    def post(cls):
        data = cls.parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if(user is None):
            return {'message' : "Invalid credentials"}, 401   
        salt = base64.b64decode(user.salt)  # decoding base64 to bytes
        password_hash = hashPassword(data['password'], salt) #password hash is in base64 format
        
        if safe_str_cmp(user.password, password_hash):
            access_token = create_access_token(identity=user.id,fresh=True)
            #refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'user': user.json()
            },200
        return {'message' : "Invalid credentials"}, 401   

class UserPassowrd(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "password", type=str, required=True, help="This field cannot be left blank!"
    )

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()
        ID = get_jwt_identity()
        user = UserModel.find_by_id(ID)

        password_new = data["password"]
        salt_new = urandom(32)

        data["password"] = hashPassword(password_new, salt_new)
        data["salt"] = base64.b64encode(salt_new)
        user.password = data['password']
        user.salt = data['salt']
        user.save_to_db()

        return {'message': 'Hasło zostało zmienione'}, 200

class UserAbout(Resource):    
    @classmethod
    @jwt_required
    def get(cls):
        ID = get_jwt_identity()
        user = UserModel.find_by_id(ID)
        return {'about' : user.about}, 200

    @classmethod
    @jwt_required
    def put(cls):
        ID = get_jwt_identity()
        user = UserModel.find_by_id(ID)
        data = cls.parser.parse_args()

        if data.get('about'):
            user.about = data['about']
            user.save_to_db()
            return {'message': 'Nowa wartość about = ' + data['about']}, 200
        else:
            return {'message': "This field cannot be left blank!"}, 404
        
        


