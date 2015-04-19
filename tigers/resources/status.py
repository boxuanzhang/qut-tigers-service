

from bson import ObjectId
from flask import g
from flask.ext.restful import Resource, abort, reqparse
from tigers.models.status import StatusHelper
from tigers.decorators.auth import login_required


class Status(Resource):

    def get(self, status_id):
        status = StatusHelper.get(ObjectId(status_id))
        if status is None:
            abort(404)
        return {
            'status': status.export_entity()
        }

    @login_required
    def delete(self, status_id):
        status = StatusHelper.get(ObjectId(status_id))
        if status is None:
            abort(404)
        if status.user != g.user:
            abort(401)
        StatusHelper.delete(ObjectId(status_id))
        return '', 204


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
    def post(self):
        args = self.post_parser.parse_args()
        status = StatusHelper.insert(g.user, **args)
        return {
            'status': status.export_entity()
        }, 201
