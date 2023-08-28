from functools import wraps
from flask import session, render_template


def check_user_login(func):
    @wraps(func)
    def check_user_login_in_session(*args, **kwargs):
        if "user_id" not in session:
            return render_template("user/login.html")
        return func(*args, **kwargs)
    return check_user_login_in_session