

import os
import jwt
import time
import hashlib
import binascii
from tigers.models.user import User, RefreshToken
from tigers import app


__all__ = [
    'parse_payload', 'generate_token', 'parse_token', 'refresh_token'
]


def parse_payload(payload):
    """Parse information from payload.

    :param payload:
    :return: (uid, nonce, exp)
    """
    return payload['uid'], payload['nonce'], payload['exp']


def _build_token(data, expire=None):
    if expire:
        data.update({
            'exp': expire
        })
    return jwt.encode(
        data,
        app.config['JWT_SECRET'],
        app.config['JWT_METHOD']
    )
    pass


def _generate_access_token(uid, expire):
    return _build_token({
        'uid': uid,
        'nonce': binascii.hexlify(os.urandom(10))
    }, expire)


def _generate_refresh_token(access, refresh_id):
    return _build_token({
        'hash': hashlib.sha1(access).hexdigest(),
        'id': refresh_id
    })


def _generate_token(uid):
    expire = int(time.time()) + app.config['JWT_EXPIRE']
    access = _generate_access_token(uid, expire)

    record = RefreshToken()
    record.save()

    refresh = _generate_refresh_token(access, str(record.id))

    return access, refresh, expire


def generate_token(user):
    """
    Generate access token.
    :param uid: string user ID
    :return: string access token
    """
    assert isinstance(user, User), 'user should be an instance of model UserBase: %r' % (user,)
    assert user.id is not None, 'user.id should not be None'

    return _generate_token(str(user.id))


def parse_token(token):
    """
    Parse payload from token.
    :param token: string access token
    :return: dict payload
    """
    return jwt.decode(token, app.config['JWT_SECRET'])


def refresh_token(user, refresh):
    assert isinstance(user, User), 'user should be an instance of UserBase: %r' % (user,)

    # Parse refresh token
    try:
        refresh_payload = parse_token(refresh)
    except jwt.DecodeError:
        return None, None, 0
    except jwt.ExpiredSignature:
        return None, None, 0

    # Calculate sha1 hash of access token
    access_hash = hashlib.sha1(user.token).hexdigest()

    # Test hash
    if refresh_payload['hash'] != access_hash:
        return None, None, 0

    # Get refresh token record
    refresh_record = RefreshToken.objects(id=refresh_payload['id'], available=True).update(set__available=False)
    if refresh_record == 0:
        return None, None, 0

    # Delete record
    RefreshToken.objects(id=refresh_payload['id']).delete()

    # Return new tokens
    return _generate_token(str(user.id))
