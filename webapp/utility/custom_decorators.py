from functools import wraps
from flask_login import current_user
from flask import jsonify

def EmailAuthRequired():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if current_user.isEmailVerified:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Email is not verified"), 403

        return decorator

    return wrapper

