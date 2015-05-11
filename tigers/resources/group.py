from bson import ObjectId
from flask.ext.restful import Resource, abort, reqparse

from .. import permission_manager
from ..models.user import GroupHelper
from ..decorators.auth import login_required
from ..utils import http_status


__all__ = [
    'Group', 'GroupList'
]


class Group(Resource):

    put_parser = reqparse.RequestParser()
    put_parser.add_argument('name', type=unicode, required=False)
    put_parser.add_argument('permissions', type=unicode, action='append', required=False)

    @login_required
    @permission_manager.permission_required('group', 'get')
    def get(self, group_id):
        group = GroupHelper.get(ObjectId(group_id))
        if not group:
            abort(http_status.HTTP_404_NOT_FOUND)

        return \
            {
                'group': group.export_entity()
            }

    @login_required
    @permission_manager.permission_required('group', 'delete')
    def delete(self, group_id):
        group = GroupHelper.get(ObjectId(group_id))
        if not group:
            abort(http_status.HTTP_404_NOT_FOUND)

        GroupHelper.delete(ObjectId(group_id))

        return '', http_status.HTTP_204_NO_CONTENT

    @login_required
    @permission_manager.permission_required('group', 'put')
    def put(self, group_id):
        group = GroupHelper.get(ObjectId(group_id))
        if not group:
            abort(http_status.HTTP_404_NOT_FOUND)

        args = self.put_parser.parse_args()
        group = GroupHelper.update(ObjectId(group_id), **args)

        return \
            {
                'group': group.export_entity()
            }


class GroupList(Resource):

    post_parser = reqparse.RequestParser()
    post_parser.add_argument('name', type=unicode, required=False)
    post_parser.add_argument('permissions', type=unicode, action='append', required=False)

    @login_required
    @permission_manager.permission_required('groups', 'get')
    def get(self):
        groups = GroupHelper.all()

        return \
            {
                'groups': [x.export_entity() for x in groups]
            }

    @login_required
    @permission_manager.permission_required('groups', 'post')
    def post(self):
        args = self.post_parser.parse_args()

        group = GroupHelper.insert(args['name'], args['permissions'])

        return \
            {
                'group': group.export_entity()
            }
