

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

        user_base = UserHelper.get(uid)
        if not user_base:
            return 'Nonexistent user or denied user', 401

        # Delete password information for security issue
        user_base.password = ''
        user_base.salt = ''

        # Prevent some actions
        user_base.delete = user_base.modify = user_base.reload = None
        user_base.save = user_base.update = None

        # For compatibility
        user_base.uid = str(user_base.id)

        # Store raw token
        user_base.token = token

        g.user = user_base

        return f(*args, **kwargs)
    return decorated_function
