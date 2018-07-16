import uuid
from functools import wraps

from flask import session, request, abort

from models.token import Token
from models.user import User


def current_user():
    uid = session.get('user_id', '')
    u = User.one(id=uid)
    return u


csrf_tokens = dict()


def csrf_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args['token']
        u = current_user()
        token = Token.one(content=token, user_id=u.id)
        if token is not None:
            # csrf_tokens.pop(token)
            return f(*args, **kwargs)
        else:
            abort(401)

    return wrapper


def new_csrf_token():
    u = current_user()
    token = str(uuid.uuid4())
    form = dict(
        content=token,
        user_id=u.id
    )
    Token.new(form)
    return token
