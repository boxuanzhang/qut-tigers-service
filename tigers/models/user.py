

import hashlib
import os
import datetime
import binascii
from bson import ObjectId
from mongoengine import *
from utils.export import ExportableMixin


class RefreshToken(Document):
    available = BooleanField(default=True, required=True)
    timestamp = DateTimeField(default=datetime.datetime.utcnow, required=True)


class Group(Document):
    name = StringField(required=True)


class User(Document, ExportableMixin):
    username = StringField(max_length=64, required=True)
    name = StringField(max_length=64, required=True)
    password = StringField(required=True)
    salt = StringField(required=True)
    groups = ListField(ReferenceField(Group))
    join_time = DateTimeField(required=True)

    _exported_fields = (
        'username', 'name', 'join_time'
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
    def verify_password(user_base, password):
        """Verify user password.

        :param user_base:
        :param password:
        :return: bool
        """
        assert isinstance(user_base, User)
        assert isinstance(password, basestring)

        return user_base.password == UserHelper.password_hash(password, user_base.salt)

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
    def insert(username, name, password, groups):
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
