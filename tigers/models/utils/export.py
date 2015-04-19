

import datetime
import inspect
from bson import ObjectId
from mongoengine import *


__all__ = [
    'ExportableMixin'
]


def dt_to_timestamp(dt):
    assert isinstance(dt, datetime.datetime)
    return int((dt - datetime.datetime(1970, 1, 1)).total_seconds())


def export_entity(obj, fields=None):
    assert isinstance(obj, (Document, EmbeddedDocument))

    def export_val(val, resolve_ref=False):
        if isinstance(val, (basestring, int, float)):
            return val

        # Handle system types
        if isinstance(val, list):
            return map(export_entity, val)
        elif isinstance(val, datetime.datetime):
            return dt_to_timestamp(val)

        # Resolve ref for exportable entity
        if resolve_ref and isinstance(val, ExportableMixin):
            return val.export_entity()

        if isinstance(val, EmbeddedDocument):
            if isinstance(val, ExportableMixin):
                return val.export_entity()
            return export_entity(val)

        if isinstance(val, Document):
            return str(val.id)

        if isinstance(val, ObjectId):
            return str(val)

        return val

    d = {}
    if fields:
        for name in fields:
            resolve_ref = False
            key = name
            if type(name) == tuple:  # Check if extra options is specified
                assert len(name) > 1, 'Tuple given but no options found'
                if type(name[1]) == bool:  # Case: (field_name, resolve_ref)
                    resolve_ref = name[1]
                    key = name[0]
                else:
                    if len(name) == 3:  # Case: (field_name, output_name, resolve_ref)
                        resolve_ref = name[2]
                    key = name[1]  # Case: (field_name, output_name)
                value = getattr(obj, name[0])
            else:
                value = getattr(obj, key)
            d[key] = export_val(value, resolve_ref)
    else:
        for name in dir(obj):
            value = getattr(obj, name)
            if name not in ('objects', 'pk') and not name.startswith('_') and \
                    not inspect.ismethod(value) and \
                    not inspect.isclass(value):
                d[name] = export_val(value)

    return d


class ExportableMixin(object):

    _exported_fields = None

    def export_entity(self):
        return export_entity(self, self._exported_fields)
