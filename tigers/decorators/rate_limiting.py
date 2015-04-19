

# Import components
from functools import wraps
from flask import request
from simplrapi import redis
from simplrapi.responses.system import RateLimitExceeded
from simplrapi.utils.response import render_response


def rate_limit(rate, bucket=None):
    """Limit API request rate.

    :param rate: requests limit every minute.
    :param bucket: rate limiting bucket.
    """

    def limit_func(f):
        slot = bucket
        if not slot:
            slot = f.__name__

        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get Redis storage key
            client = ':'.join(request.access_route)
            key = 'Rate_%s_%s' % (slot, client)

            # Check current rate
            current = redis.llen(key)
            if current >= rate:
                return render_response(RateLimitExceeded,
                                       '[Client %s - Bucket %s - Limit %d - Current %d]'
                                       % (client, slot, rate, current))

            # Update record
            if not redis.exists(key):
                pipe = redis.pipeline()
                pipe.rpush(key, '')
                pipe.expire(key, 60)
                pipe.execute()
            else:
                redis.rpushx(key, '')
            return f(*args, **kwargs)

        return decorated_function

    return limit_func
