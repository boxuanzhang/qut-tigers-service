

from bson import ObjectId
from mongoengine import QuerySet, Q
import base64


__all__ = [
    'paging'
]


def paging(queryset, pos_key, args, reverse=True):
    assert isinstance(queryset, QuerySet)
    assert isinstance(pos_key, basestring)

    # Get cursor and limit from querystring
    cursor = args.get('_after', None)
    limit = int(args.get('_per_page', 10)) + 1  # plus 1 for next page checking

    # Perform query
    queryset = queryset.order_by('-' + pos_key if reverse else pos_key, '-id')
    if cursor is None:
        queryset = queryset.filter()
    else:
        _pos, _id = cursor.split(':')
        _pos = base64.urlsafe_b64decode(_pos.encode('ascii')).decode('utf-8')
        _id = base64.urlsafe_b64decode(_id.encode('ascii')).decode('utf-8')
        # _pos = int(_pos)
        _id = ObjectId(_id)
        operator = '__lt' if reverse else '__gt'
        key_q = {
            pos_key + operator: _pos
        }
        id_q = {
            pos_key: _pos,
            'id' + operator: _id
        }
        queryset = queryset.filter(Q(**key_q) | Q(**id_q))

    queryset = queryset.limit(limit)

    result = list(queryset)
    cursor = {}
    if len(result) == limit:
        result.pop()
        last = result[-1]
        key_val = unicode(reduce(getattr, pos_key.split('__'), last)).encode('utf-8')
        id_val = unicode(last.id).encode('utf-8')
        cursor['after'] = '%s:%s' % (base64.urlsafe_b64encode(key_val), base64.urlsafe_b64encode(id_val))

    return result, {
        '_paging': cursor
    }
