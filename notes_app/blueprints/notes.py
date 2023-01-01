from flask import Blueprint, render_template, request, redirect, url_for, Flask
from flask_login import login_required, current_user
from notes_app.data import databaseHelper
from notes_app.forms.notes import NoteForm
from werkzeug.exceptions import Unauthorized
import datetime

bp = Blueprint("notes", __name__)

def register(app: Flask):
    app.register_blueprint(bp)


@bp.route("/", methods=["GET", "POST"])
def index():    
    """ 
    Note dashboard for the website, accessible after logging in
    """

    form = NoteForm()

    # POST request
    if form.validate_on_submit():

        # if user isn't logged in
        if not current_user.is_authenticated:
            raise Unauthorized()
        
        # gathering data from note-form 
        data = request.form
        print(data)
        title = data["title"]
        desc = data["description"]
        
        # inserting submitted note into the database
        databaseHelper.insert_note(current_user.user_id, title, desc)

        return redirect(url_for("notes.index"))

    # fetching every note stored in the database
    notes = databaseHelper.all_notes(current_user.user_id) if current_user.is_authenticated else None

    # GET request
    return render_template("main.html", notes = notes, user = current_user, form = form)
    

@bp.route("/delete/<int:note_id>", methods=["DELETE", "GET"])
@login_required
def delete(note_id):

    if current_user.is_authenticated:
        databaseHelper.delete_note(note_id, current_user.user_id)

    return redirect(url_for("notes.index"))


@bp.route("/edit/<int:note_id>", methods=["POST", "GET"])
@login_required
def edit(note_id):
    
    form = NoteForm()

    # POST request
    if form.validate_on_submit():
        data = request.form
        title = data["title"]
        desc = data["description"]

        # updating attribute's values in database
        databaseHelper.edit_note(title, desc, note_id)
    
        return redirect(url_for("notes.index"))

    # fetching the updated note from database
    current_note = databaseHelper.fetch_note(note_id)[0]

    # GET request
    return render_template("./forms/edit.html", note = current_note, user = current_user, form = form)


@bp.app_template_filter("format_datetime")
def _format_datetime(date: datetime.datetime):
    return date.strftime("%d %b %y, at %H:%M")
