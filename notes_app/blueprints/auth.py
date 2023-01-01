from flask import Blueprint, render_template, redirect, url_for, request, flash, Flask
from flask_login import login_user, logout_user, login_required, current_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from notes_app.data import databaseHelper
from notes_app.forms.login import *
from notes_app.forms.signup import *

bp = Blueprint("auth", __name__)


def register(app: Flask):
    """ 
    registers the blueprint in the flask app with login authentication
    """
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(email):
        return databaseHelper.fetch_user_by_email(email)

    app.register_blueprint(bp, url_prefix="/")


@bp.route("/login", methods=["GET", "POST"])
def login():
    
    # checking if the user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for("notes.index"))

    form = LogInForm()

    # POST request
    if form.validate_on_submit():

        data = request.form

        email = data["email"]
        password = data["password"]

        # fetching user's registered details from database
        user = databaseHelper.fetch_user_by_email(email)

        # user exists or password matches conditions
        if user is None or not check_password_hash(user.password_hash, password):
            flash("Login failed. Incorrect email or password.", "error")

            return redirect(url_for("auth.login"))

        # login the user if authentication is successful
        login_user(user)

        return redirect(url_for("notes.index"))

    # GET request
    return render_template("./forms/login.html", user = current_user, form = form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("notes.index"))


@bp.route("/signup", methods=["GET", "POST"])
def signup():

    form = SignUpForm()

    # POST request
    if form.validate_on_submit():

        data = request.form

        # gathering data from signup form if validated
        username = data["username"]
        email = data["email"]
        password = data["password"]
        confirm_password = data["confirm_password"]

        # matching provided passwords
        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for("auth.signup"))

        # checking if email is already registered
        is_email_available = databaseHelper.is_email_available(email)

        if not is_email_available:
            flash("The email has already been taken.", "error")
            return redirect(url_for("auth.signup"))

        # registering user by storing data into the database
        databaseHelper.register_user(
            username = username,
            email = email,
            password = generate_password_hash(password)
        )

        # auto login at sign-up
        user = databaseHelper.fetch_user_by_email(email)
        login_user(user)

        return redirect(url_for("auth.login"))
    
    # GET request
    return render_template("./forms/signup.html", user = current_user, form = form)
    