

from flask.ext.restful import Resource, abort, reqparse
from tigers.models.user import UserHelper
from tigers.utils.auth import generate_token


class Auth(Resource):

    get_parser = reqparse.RequestParser()
    get_parser.add_argument('username', type=unicode, required=True)
    get_parser.add_argument('password', type=unicode, required=True)

    post_parser = reqparse.RequestParser()
    post_parser.add_argument('username', type=unicode, required=True)
    post_parser.add_argument('password', type=unicode, required=True)
    post_parser.add_argument('name', type=unicode, required=True)

    def get(self):
        args = self.get_parser.parse_args()
        user = UserHelper.get_by_username(args['username'])
        if not UserHelper.verify_password(user, args['password']):
            return '', 401

        # Generate access token
        access, refresh, expire = generate_token(user)

        return {
            'access_token': access,
            'refresh_token': refresh,
            'expire': expire,
            'user': user.export_entity()
        }, 200

    def post(self):
        args = self.post_parser.parse_args()
        user = UserHelper.insert(args['username'], args['name'], args['password'], [])

        # Generate access token
        access, refresh, expire = generate_token(user)

        return {
            'access_token': access,
            'refresh_token': refresh,
            'expire': expire,
            'user': user.export_entity()
        }, 201
