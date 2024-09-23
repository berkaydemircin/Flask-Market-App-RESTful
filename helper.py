import os
from requests import request
from flask import Flask, redirect, session, render_template, flash, url_for
from werkzeug.utils import secure_filename
from functools import wraps

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def displayError(text, code):
    return render_template("error.html", text=text, code=code), code
