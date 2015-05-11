from flask.ext.restful import Resource, abort, reqparse

from .. import app, permission_manager
from ..models.user import UserHelper
from ..utils.auth import generate_token
from ..utils import http_status


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
        if not user or not UserHelper.verify_password(user, args['password']):
            return '', 401

        # Generate access token
        access, refresh, expire = generate_token(user)

        # Get permissions
        if permission_manager.is_superuser(user):
            permissions = permission_manager.get_registered_permissions()
        else:
            permissions = []
            for group in user.groups:
                permissions += group.permissions
            user.permissions = set(permissions)

        return \
            {
                'access_token': access,
                'refresh_token': refresh,
                'expire': expire,
                'user': user.export_entity(),
                'permissions': permissions
            }, http_status.HTTP_200_OK

    def post(self):
        # Only allowed in debug mode
        if not app.debug:
            abort(404)

        args = self.post_parser.parse_args()
        user = UserHelper.insert(args['username'], args['name'], args['password'], [])

        # Generate access token
        access, refresh, expire = generate_token(user)

        return \
            {
                'access_token': access,
                'refresh_token': refresh,
                'expire': expire,
                'user': user.export_entity()
            }, http_status.HTTP_201_CREATED
