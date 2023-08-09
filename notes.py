from config import db
from flask import abort, make_response
from models import Note, Person, note_schema


# Function to read one note
def read_one(note_id):
    note = Note.query.get(note_id)
    if note is not None:
        return note_schema.dump(note), 200
    else:
        abort(
            404,
            f"Note do not exist"
        )

# Function to update one note

def update(note_id, note):
    existing_note = Note.query.get(note_id)
    if existing_note:
        update_note = note_schema.load(note, session=db.session)
        existing_note.content = update_note.content
        db.session.merge(existing_note)
        db.session.commit()
        return note_schema.dump(note), 201
    else:
        abort(
            401,
            f"Could not update note with id {note_id}"
        )

# Function to delete one note
def delete(note_id):
    existing_note = Note.query.get(note_id)
    if existing_note:
        db.session.delete(existing_note)
        db.session.commit()
        return make_response(
           f"Note with id:{note_id} successfully deleted", 200
        )
    else:
        abort(
            401,
            f"Could not delete note with id: {note_id}"
        )
        

# function to create a note
def create(note):
    person_id = note.get("person_id")
    person = Person.query.get(person_id)
    if person:
        new_note =note_schema.load(note, session=db.session)
        person.notes.append(new_note)
        db.session.commit()
        return note_schema.dump(new_note), 201
    else:
        abort(
            401,
            f"Person not found"
        )
