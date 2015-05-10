from bson import ObjectId
from flask import g
from flask.ext.restful import Resource, abort, reqparse

from .. import permission_manager
from ..models.status import StatusHelper
from ..decorators.auth import login_required
from ..utils import http_status


class Status(Resource):
    def get(self, status_id):
        status = StatusHelper.get(ObjectId(status_id))
        if status is None:
            abort(http_status.HTTP_404_NOT_FOUND)
        return \
            {
                'status': status.export_entity()
            }

    @login_required
    @permission_manager.permission_required('status', 'delete')
    def delete(self, status_id):
        status = StatusHelper.get(ObjectId(status_id))
        if status is None:
            abort(http_status.HTTP_404_NOT_FOUND)
        if status.user != g.user:
            abort(http_status.HTTP_403_FORBIDDEN)
        StatusHelper.delete(ObjectId(status_id))
        return '', http_status.HTTP_204_NO_CONTENT


class StatusList(Resource):
    get_parser = reqparse.RequestParser()
    get_parser.add_argument('_after', type=unicode, default=None)
    get_parser.add_argument('_per_page', type=int, default=20)

    post_parser = reqparse.RequestParser()
    post_parser.add_argument('title', type=unicode, required=True)
    post_parser.add_argument('subtitle', type=unicode, required=True)
    post_parser.add_argument('content', type=unicode, required=True)
    post_parser.add_argument('photos', type=unicode, action='append', required=True, default=[])

    def get(self):
        results, paging = StatusHelper.latest(self.get_parser.parse_args())
        res = {
            'statuses': map(lambda x: x.export_entity(), results)
        }
        res.update(paging)
        return res

    @login_required
    @permission_manager.permission_required('statuses', 'post')
    def post(self):
        args = self.post_parser.parse_args()
        status = StatusHelper.insert(g.user, **args)
        return \
            {
                'status': status.export_entity()
            }, http_status.HTTP_201_CREATED
