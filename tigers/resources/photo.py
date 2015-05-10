from bson import ObjectId
from flask import g, request
from flask.ext.restful import Resource, abort, reqparse

from .. import api, permission_manager
from ..models.photo import PhotoHelper
from ..models.user import UserHelper
from ..decorators.auth import login_required
from ..utils.qiniu import verify_callback, get_image_upload_params
from ..utils import http_status


class Photo(Resource):
    def get(self, photo_id):
        photo = PhotoHelper.get(ObjectId(photo_id))
        if photo is None:
            abort(http_status.HTTP_404_NOT_FOUND)
        return {
            'photo': photo.export_entity()
        }

    @login_required
    @permission_manager.permission_required('photo', 'delete')
    def delete(self, photo_id):
        photo = PhotoHelper.get(ObjectId(photo_id))
        if photo is None:
            abort(http_status.HTTP_404_NOT_FOUND)
        if photo.user != g.user:
            abort(http_status.HTTP_403_FORBIDDEN)
        PhotoHelper.delete(ObjectId(photo_id))
        return '', http_status.HTTP_204_NO_CONTENT


class PhotoToken(Resource):
    get_parser = reqparse.RequestParser()
    get_parser.add_argument('description', type=unicode, required=True)

    @login_required
    @permission_manager.permission_required('photo_token', 'get')
    def get(self):
        args = self.get_parser.parse_args()
        upload_params = get_image_upload_params(api.url_for(PhotoToken, _external=True), extra={
            'uid': g.user.uid,
            'desc': args['description']
        })

        return upload_params

    def post(self):
        body = request.stream.readline()

        data = verify_callback(request.headers.get('Authorization', ''), request.script_root + request.path, body)

        if not data:
            abort(http_status.HTTP_403_FORBIDDEN)

        key = data.get('key')
        uid = data.get('uid')
        desc = data.get('desc')

        # Get user document
        user_base = UserHelper.get(uid)
        if not user_base:
            abort(http_status.HTTP_403_FORBIDDEN)

        photo = PhotoHelper.insert(user_base, key, desc)

        return \
            {
                'photo': photo.export_entity()
            }, http_status.HTTP_201_CREATED
