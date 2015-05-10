

# Import components
import jwt
from functools import wraps
from flask import request, g
from tigers.models.user import UserHelper
from tigers.utils.auth import parse_token, parse_payload


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        authorization = request.headers.get('Authorization', '')
        token = authorization[7:]

        # Length check
        if len(token) <= 0:
            return 'Authorization header required', 401

        # Decode
        try:
            payload = parse_token(token)
        except jwt.DecodeError, jwt.ExpiredSignatureError:
            return 'Token parse error', 401

        # Set up user information
        uid, _, _ = parse_payload(payload)

        user = UserHelper.get(uid)
        if not user:
            return 'Nonexistent user or denied user', 401

        # Delete password information for security issue
        user.password = ''
        user.salt = ''

        # Prevent some actions
        user.delete = user.modify = user.reload = None
        user.save = user.update = None

        # For compatibility
        user.uid = str(user.id)

        # Store raw token
        user.token = token

        # Get permissions
        permissions = []
        for group in user.groups:
            permissions += group.permissions
        user.permissions = set(permissions)

        g.user = user

        return f(*args, **kwargs)
    return decorated_function
