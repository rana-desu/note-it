from flask import render_template, Flask
from flask_login import current_user

def page_not_found(e):
    error_code = 404
    return render_template("errors.html", error = error_code, user = current_user), 404

def internal_server_error(e):
    error_code = 500    
    return render_template("errors.html", error = error_code, user = current_user), 500
    