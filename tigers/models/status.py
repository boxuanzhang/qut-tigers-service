import datetime
from bson import ObjectId
from mongoengine import *
from user import User
from .utils.pagination import paging
from .utils.export import ExportableMixin


__all__ = [
    'Status', 'StatusHelper'
]


class Status(Document, ExportableMixin):
    title = StringField(required=True)
    subtitle = StringField(required=True)
    content = StringField(required=True)
    photos = ListField(StringField(), default=list, required=True)
    timestamp = DateTimeField(required=True)
    user = ReferenceField(User, required=True)

    _exported_fields = (
        'id', 'title', 'subtitle', 'content', 'timestamp', 'user'
    )

    def export_entity(self):
        entity = super(Status, self).export_entity()
        entity.update({
            'photos': self.photos
        })
        return entity


class StatusHelper(object):
    """Helper for Status document."""

    @staticmethod
    def insert(user, title, subtitle, content, photos):
        """Insert a Status document.

        :param title:
        :param subtitle:
        :param content:
        :param user:
        :return: Status document inserted
        """
        status = Status()
        status.title = title
        status.subtitle = subtitle
        status.content = content
        status.photos = photos
        status.user = user
        status.timestamp = datetime.datetime.utcnow()
        status.save()
        return status

    @staticmethod
    def get(status_id):
        """Get Status document.

        :param status_id:
        :return:
        """
        return Status.objects(id=status_id).first()

    @staticmethod
    def latest(args):
        """Get latest Status documents.

        :param args:
        :return:
        """
        return paging(Status.objects(), 'timestamp', args)

    @staticmethod
    def delete(status_id):
        """Delete Status document.

        :param status_id:
        :return:
        """
        assert isinstance(status_id, ObjectId)
        Status.objects(id=status_id).delete()
