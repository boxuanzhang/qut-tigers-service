

from flask import g
from collections import defaultdict
from functools import wraps
from copy import deepcopy
from .. import app


class PermissionsManager(object):

    _entry_registry = defaultdict(set)

    def permission_required(self, category, entry):
        # Add entry to registry
        self._entry_registry[category].add(entry)

        permission_key = '%s:%s' % (category, entry)

        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                assert hasattr(g, 'user'), 'login_required() decorator must be applied before permission_required()'

                if g.user.username == app.config['SUPER_USER']:
                    return f(*args, **kwargs)

                if permission_key not in g.user.permissions:
                    return 'Permission denied', 401
                return f(*args, **kwargs)
            return decorated_function
        return decorator

    def get_entry_registry(self):
        return deepcopy(self._entry_registry)
