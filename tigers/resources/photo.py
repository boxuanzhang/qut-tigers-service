__author__ = 'Microdog <zhukainan@imjidu.com>'

from tigers import api
from bson import ObjectId
from flask import g, request
from flask.ext.restful import Resource, abort, reqparse
from tigers.models.photo import PhotoHelper
from tigers.models.user import UserHelper
from tigers.decorators.auth import login_required
from tigers.utils.qiniu import verify_callback, get_image_upload_params


class Photo(Resource):

    def get(self, photo_id):
        photo = PhotoHelper.get(ObjectId(photo_id))
        if photo is None:
            abort(404)
        return {
            'status': photo.export_entity()
        }

    @login_required
    def delete(self, photo_id):
        photo = PhotoHelper.get(ObjectId(photo_id))
        if photo is None:
            abort(404)
        if photo.user != g.user:
            abort(401)
        PhotoHelper.delete(ObjectId(photo_id))
        return '', 204


class PhotoToken(Resource):

    get_parser = reqparse.RequestParser()
    get_parser.add_argument('description', type=unicode, required=True)

    @login_required
    def get(self):
        args = self.get_parser.parse_args()
        upload_params = get_image_upload_params(api.url_for(PhotoToken, _external=True), extra={
            'uid': g.user.uid,
            'desc': args['description']
        })

        return upload_params, 200

    @login_required
    def post(self):
        body = request.stream.readline()

        data = verify_callback(request.headers.get('Authorization', ''), request.script_root + request.path, body)

        if not data:
            abort(401)

        key = data.get('key')
        uid = data.get('uid')
        desc = data.get('desc')

        # Get user document
        user_base = UserHelper.get(uid)
        if not user_base:
            abort(401)

        photo = PhotoHelper.insert(user_base, key, desc)

        return {
            'photo': photo.export_entity()
        }, 201
