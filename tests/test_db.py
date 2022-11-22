"""
Database level tests
"""

import flask

from notes_app.data import databaseHelper


def test_create_fetch_user(app: flask.Flask):
    """
    Test user creation and retrieval
    """
    with app.app_context():
        databaseHelper.register_user(
            "user1",
            "user1@somewhere.com",
            "user1_password")

    with app.app_context():
        databaseHelper.register_user(
            "user2",
            "user2@somewhere.com",
            "user2_password")

    with app.app_context():
        user1 = databaseHelper.fetch_user_by_email("user1@somewhere.com")
        user2 = databaseHelper.fetch_user_by_email("user2@somewhere.com")

    assert user1.user_id is not None
    assert user1.username == "user1"
    assert user1.get_id() == user1.email == "user1@somewhere.com"
    assert user1.password_hash == "user1_password"

    assert user2.user_id is not None
    assert user2.username == "user2"
    assert user2.get_id() == user2.email == "user2@somewhere.com"
    assert user2.password_hash == "user2_password"

    # Make sure we can fetch the same users by IDs
    with app.app_context():
        user1_by_id = databaseHelper.fetch_user_by_id(user1.user_id)
        user2_by_id = databaseHelper.fetch_user_by_id(user2.user_id)

    assert user1 == user1_by_id
    assert user2 == user2_by_id

def test_create_note(app: flask.Flask):
    """
    Test note creation
    """
    with app.app_context():
        databaseHelper.register_user(
            "user1",
            "user1@somewhere.com",
            "user1_password")
        user1 = databaseHelper.fetch_user_by_email("user1@somewhere.com")

    with app.app_context():
        databaseHelper.register_user(
            "user2",
            "user2@somewhere.com",
            "user2_password")
        user2 = databaseHelper.fetch_user_by_email("user2@somewhere.com")

    with app.app_context():
        databaseHelper.insert_note(
            user1.user_id,
            "Example note 1",
            "I wonder what should go here...",
        )
        
        databaseHelper.insert_note(
            user1.user_id,
            "Example note 2",
            "I wonder what could go here...",
        )

        databaseHelper.insert_note(
            user2.user_id,
            "Dummy note",
            "Dummy body",
        )
        
        databaseHelper.insert_note(
            user2.user_id,
            "Sample note",
            "Sample body",
        )

    with app.app_context():
        user1_notes = databaseHelper.all_notes(user1.user_id)
        user2_notes = databaseHelper.all_notes(user2.user_id)

    assert len(user1_notes) == 2
    assert len(user2_notes) == 2

    user1_note1, user1_note2 = sorted(user1_notes, key = lambda note: note.date_created)
    user2_note1, user2_note2 = sorted(user2_notes, key = lambda note: note.date_created)

    assert user1_note1.owner_id == user1_note2.owner_id == user1.user_id
    assert user2_note1.owner_id == user2_note2.owner_id == user2.user_id

    assert user1_note1.title == "Example note 1"
    assert user1_note2.title == "Example note 2"
    assert user2_note1.title == "Dummy note"
    assert user2_note2.title == "Sample note"

    assert user1_note1.description == "I wonder what should go here..."
    assert user1_note2.description == "I wonder what could go here..."
    assert user2_note1.description == "Dummy body"
    assert user2_note2.description == "Sample body"
