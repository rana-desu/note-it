from flask import Blueprint, render_template, request, redirect, url_for, Flask
from flask_login import login_required, current_user
from notes_app.data import databaseHelper
from werkzeug.exceptions import Unauthorized
import datetime

bp = Blueprint("notes", __name__)

def register(app: Flask):
    app.register_blueprint(bp)


@bp.route("/", methods=["GET", "POST"])
def index():    
    
    if request.method == "POST":
        if not current_user.is_authenticated:
            raise Unauthorized()
        
        data = request.form
        title = data["title"]
        desc = data["desc"]

        
        # inserting submitted note into database
        databaseHelper.insert_note(current_user.user_id, title, desc)

        return redirect(url_for("notes.index"))

    # fetching every note stored in the database
    notes = databaseHelper.all_notes(current_user.user_id) if current_user.is_authenticated else None

    return render_template("main.html", notes = notes, user = current_user)
    

@bp.route("/delete/<int:note_id>", methods=["DELETE", "GET"])
@login_required
def delete(note_id):

    if current_user.is_authenticated:
        databaseHelper.delete_note(note_id, current_user.user_id)

    return redirect(url_for("notes.index"))


@bp.route("/edit/<int:note_id>", methods=["POST", "GET"])
@login_required
def edit(note_id):
    
    if request.method == "POST":
        data = request.form
        title = data["title"]
        desc = data["desc"]

        # updating attribute's values in database
        databaseHelper.edit_note(title, desc, note_id)
    
        return redirect(url_for("notes.index"))

    # fetching the updated note from database
    current_note = databaseHelper.fetch_note(note_id)[0]

    return render_template("./forms/edit.html", note = current_note, user = current_user)


@bp.app_template_filter("format_datetime")
def _format_datetime(date: datetime.datetime):
    return date.strftime("%d %b %y, at %H:%M")