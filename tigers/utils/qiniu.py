


import json
import hashlib
import hmac
import base64
import time
import urlparse
import datetime
from tigers import app


UPLOAD_URL = app.config['QINIU_UPLOAD_URL']
DOWNLOAD_URL = app.config['QINIU_DOWNLOAD_URL']


def _token(data):
    data = data.encode('utf-8')
    return base64.urlsafe_b64encode(hmac.new(app.config['QINIU_SECRET_KEY'], data, hashlib.sha1).digest())


def _generate_upload_token(upload_policy):
    assert type(upload_policy) == dict

    put_policy = json.dumps(upload_policy, separators=(',', ':')).encode('utf-8')
    encoded_put_policy = base64.urlsafe_b64encode(put_policy)

    encoded_sign = _token(encoded_put_policy)

    return '%s:%s:%s' % (app.config['QINIU_ACCESS_KEY'], encoded_sign, encoded_put_policy)


def _generate_download_token(url):
    assert isinstance(url, basestring)

    encoded_sign = _token(url)

    return '%s:%s' % (app.config['QINIU_ACCESS_KEY'], encoded_sign)


def verify_callback(header, path, body):
    authstr = header[5:]
    if len(authstr) <= 0:
        app.logger.debug('Qiniu callback sign error: wrong length')
        return None

    section = authstr.split(':')
    if not len(section) == 2:
        app.logger.debug('Qiniu callback sign error: wrong sections')
        return None

    access_key, sign = section
    if not access_key == app.config['QINIU_ACCESS_KEY']:
        app.logger.debug('Qiniu callback sign error: wrong access key')
        return None

    data = '\n'.join((path, body))
    encoded_sign = _token(data)
    if not encoded_sign == sign:
        app.logger.debug('Qiniu callback sign error: wrong signature')
        return None

    body = urlparse.parse_qs(body)
    key = body.get('key')[0]
    hashv = body.get('hash')[0]
    extra = body.get('extra', [None])[0]

    data = {
        'key': key,
        'hash': hashv
    }

    if extra:
        data.update(json.loads(base64.urlsafe_b64decode(extra)))

    return data


def get_upload_params(callback_url, expire, mime=None, extra=None):
    assert type(extra) == dict

    policy = {
        'scope': app.config['QINIU_SCOPE'],
        'deadline': int(time.time() + expire),
        'callbackUrl': callback_url,
        'callbackBody': 'hash=$(hash)&key=$(key)'
    }

    # Encode extra data
    if extra:
        extra = json.dumps(extra)
        encoded_extra = base64.urlsafe_b64encode(extra)
        policy['callbackBody'] += '&extra=' + encoded_extra

    if mime:
        policy['detectMime'] = 0
        policy['mimeLimit'] = mime

    return {
        'type': 'qiniu_form',
        'url': UPLOAD_URL,
        'token': _generate_upload_token(policy)
    }


def get_download_url(key, query=None, expire_in_day=1):
    assert isinstance(key, basestring)
    assert not query or type(query) == list
    assert type(expire_in_day) == int

    if not query:
        query = []

    query.append('e=%s' % (int(datetime.date.today().strftime('%s')) + expire_in_day * 86400 + 3600,))

    querystring = '&'.join(query)
    url = '%s/%s?%s' % (DOWNLOAD_URL, key, querystring)

    token = _generate_download_token(url)

    return '%s&token=%s' % (url, token)


def get_image_upload_params(callback_url, extra=None):
    """Get image upload params.

    :param callback_url:
    :param extra:
    :return: param dict
    """
    return {
        'upload': get_upload_params(callback_url, 600, mime='image/png;image/jpeg', extra=extra)
    }


def get_image_url(key, size=None, mode=4):
    """Get image download url.

    :param key: file key
    :param size: None or tuple of scaled width and height
    :param mode: scale mode(default 4) only applied if size is not None
    :return: download url
    """
    assert isinstance(key, basestring)
    assert not size or type(size) == tuple
    assert not size or len(size) == 2
    assert type(mode) == int
    assert 0 <= mode <= 5

    query = None
    if size:
        w, h = size
        query = [
            'imageView2/%s/w/%s/h/%s' % (mode, w, h)
        ]
    return get_download_url(key, query)
