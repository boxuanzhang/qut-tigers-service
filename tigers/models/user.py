import hashlib
import os
import datetime
import binascii
from bson import ObjectId
from mongoengine import *
from .utils.export import ExportableMixin
from .utils.pagination import paging


__all__ = [
    'RefreshToken', 'Group', 'User', 'UserHelper'
]


class RefreshToken(Document):
    available = BooleanField(default=True, required=True)
    timestamp = DateTimeField(default=datetime.datetime.utcnow, required=True)


class Group(Document, ExportableMixin):
    name = StringField(required=True)
    permissions = ListField(StringField(), default=list)

    _exported_fields = (
        'id', 'name', 'permissions'
    )


class User(Document, ExportableMixin):
    username = StringField(max_length=64, unique=True, required=True)
    name = StringField(max_length=64, required=True)
    password = StringField(required=True)
    salt = StringField(required=True)
    groups = ListField(ReferenceField(Group))
    description = StringField(required=False)
    join_time = DateTimeField(required=True)

    _exported_fields = (
        'id', 'username', 'name', 'join_time', 'description'
    )


class UserHelper(object):
    """Helper for User document."""

    @staticmethod
    def password_hash(password, salt):
        return hashlib.sha256(password + salt).hexdigest()

    @staticmethod
    def get(user_id):
        assert isinstance(user_id, (basestring, ObjectId))
        return User.objects(id=user_id).first()

    @staticmethod
    def get_by_username(username):
        return User.objects(username=username).first()

    @staticmethod
    def all(paging_args):
        return paging(User.objects(), 'id', paging_args)

    @staticmethod
    def verify_password(user, password):
        """Verify user password.

        :param user:
        :param password:
        :return: bool
        """
        assert isinstance(user, User)
        assert isinstance(password, basestring)

        return user.password == UserHelper.password_hash(password, user.salt)

    @staticmethod
    def update_password(user_id, password):
        """Update password.

        :param user_id:
        :param password:
        :return:
        """
        assert isinstance(user_id, ObjectId)
        assert isinstance(password, basestring)

        salt = binascii.hexlify(os.urandom(32))
        password = UserHelper.password_hash(password, salt)

        User.objects(id=user_id).update(set__salt=salt, set__password=password)

    @staticmethod
    def update(user_id, **kwargs):
        """Update user.

        :param user_id:
        :param kwargs:
        :return: updated user document
        """
        update_kwargs = {
            'new': True, 'upsert': False
        }

        if 'password' in kwargs:
            assert isinstance(kwargs['password'], basestring)

            salt = binascii.hexlify(os.urandom(32))
            password = UserHelper.password_hash(kwargs['password'], salt)

            update_kwargs['set__salt'] = salt
            update_kwargs['set__password'] = password

        if 'groups' in kwargs:
            assert isinstance(kwargs['groups'], list)

            update_kwargs['set__groups'] = kwargs['groups']

        if 'name' in kwargs:
            assert isinstance(kwargs['name'], basestring)

            update_kwargs['set__name'] = kwargs['name']

        if 'description' in kwargs:
            assert isinstance(kwargs['description'], basestring)

            update_kwargs['set__description'] = kwargs['description']

        return User.objects(id=user_id).modify(**update_kwargs)

    @staticmethod
    def insert(username, name, password, groups=None, description=''):
        if not groups:
            groups = []

        # Prepare password
        salt = binascii.hexlify(os.urandom(32))
        salted_password = UserHelper.password_hash(password, salt)

        # UserBase
        user_base = User()
        user_base.username = username
        user_base.name = name
        user_base.groups = groups
        user_base.password = salted_password
        user_base.salt = salt
        user_base.join_time = datetime.datetime.utcnow()
        user_base.description = description
        user_base.save()

        return user_base

    @staticmethod
    def delete(user_id):
        """Delete UserBase document from database.

        :param user_id:
        :return:
        """
        assert isinstance(user_id, ObjectId)

        User.objects(id=user_id).delete()
