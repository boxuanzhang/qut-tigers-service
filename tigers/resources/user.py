from bson import ObjectId
from flask.ext.restful import Resource, abort, reqparse

from .. import permission_manager
from ..models.user import UserHelper
from ..decorators.auth import login_required


class User(Resource):

    put_parser = reqparse.RequestParser()
    put_parser.add_argument('name', type=unicode, required=False)
    put_parser.add_argument('password', type=unicode, required=False)
    put_parser.add_argument('groups', type=ObjectId, action='append', required=False)
    put_parser.add_argument('description', type=unicode, required=False)

    def get(self, user_id):
        user = UserHelper.get(ObjectId(user_id))
        if user is None:
            abort(404)
        return {
            'user': user.export_entity()
        }

    @login_required
    @permission_manager.permission_required('user', 'delete')
    def delete(self, user_id):
        user = UserHelper.get(ObjectId(user_id))
        if user is None:
            abort(404)
        r = UserHelper.delete(ObjectId(user_id))
        return '', 204

    @login_required
    @permission_manager.permission_required('user', 'put')
    def put(self, user_id):
        args = self.put_parser.parse_args()
        user = UserHelper.update(ObjectId(user_id), **args)
        return {
            'user': user.export_entity()
        }


class UserList(Resource):

    get_parser = reqparse.RequestParser()
    get_parser.add_argument('_after', type=unicode, default=None)
    get_parser.add_argument('_per_page', type=int, default=20)

    post_parser = reqparse.RequestParser()
    post_parser.add_argument('username', type=unicode, required=True)
    post_parser.add_argument('password', type=unicode, required=True)
    post_parser.add_argument('name', type=unicode, required=True)

    @login_required
    @permission_manager.permission_required('users', 'get')
    def get(self):
        results, paging = UserHelper.all(self.get_parser.parse_args())

        response = {
            'users': map(lambda x: x.export_entity(), results)
        }
        response.update(paging)

        return response

    @login_required
    @permission_manager.permission_required('users', 'post')
    def post(self):
        args = self.post_parser.parse_args()
        user = UserHelper.insert(args['username'], args['name'], args['password'], [])

        return {
            'user': user.export_entity()
        }
