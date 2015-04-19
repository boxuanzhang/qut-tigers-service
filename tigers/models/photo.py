

import datetime
from mongoengine import *
from user import User
from utils.export import ExportableMixin
from tigers.utils.qiniu import get_image_url


__all__ = [
    'Photo', 'PhotoHelper'
]


class Photo(Document, ExportableMixin):
    key = StringField(required=True)
    description = StringField(default='', required=True)
    timestamp = DateTimeField(required=True)
    user = ReferenceField(User, required=True)

    _exported_fields = (
        'id', 'description', 'timestamp', 'user'
    )

    def export_entity(self):
        entity = super(Photo, self).export_entity()
        entity.update(
            {
                'url': get_image_url(self.key, (320, 320)),
                'url_large': get_image_url(self.key, (640, 640)),
                'url_hd': get_image_url(self.key)
            }
        )
        return entity


class PhotoHelper(object):
    """Helper for Photo document."""

    @staticmethod
    def insert(user, key, description=''):
        """Insert Photo document.

        :param user:
        :param key:
        :param description:
        :return:
        """
        photo = Photo()
        photo.user = user
        photo.key = key
        photo.description = description
        photo.timestamp = datetime.datetime.utcnow()
        photo.save()
        return photo

    @staticmethod
    def get(photo_id):
        """Get Photo document by id.

        :param photo_id:
        :return:
        """
        return Photo.objects(id=photo_id).first()

    @staticmethod
    def delete(photo_id):
        """Delete Photo document.

        :param photo_id:
        :return:
        """
        Photo.objects(id=photo_id).delete()
