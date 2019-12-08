from flask import url_for,redirect,session
from functools import wraps



def is_login(func):
    @wraps(func)
    def check_login(*args,**kwargs):
        authority = session.get('authority')
        if authority:
            func(*args,**kwargs)
        else:
            redirect(url_for('admin.login'))
    return check_login



