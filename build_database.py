from datetime import datetime
from config import app, db
from models import Person, Note

PEOPLE_NOTES = [
    {
        "lname": "Fairy",
        "fname": "Tooth",
        "notes": [
            ("I brush my teeth after each meal.", "2022-01-06 17:10:24"),
            ("The other day a friend said, I have big teeth.", "2022-03-05 22:17:54"),
            ("Do you pay per gram?", "2022-03-05 22:18:10"),
        ],
    },
    {
        "lname": "Ruprecht",
        "fname": "Knecht",
        "notes": [
            ("I swear, I'll do better this year.", "2022-01-01 09:15:03"),
            ("Really! Only good deeds from now on!", "2022-02-06 13:09:21"),
        ],
    },
    {
        "lname": "Bunny",
        "fname": "Easter",
        "notes": [
            ("Please keep the current inflation rate in mind!", "2022-01-07 22:47:54"),
            ("No need to hide the eggs this time.", "2022-04-06 13:03:17"),
        ],
    },
]

# Initialize the context for our Flask application 'app'
with app.app_context():
    # Drop all tables from the database, essentially clearing it
    db.drop_all()

    # Create all tables based on the models (like 'Person' and 'Note') defined in the app
    db.create_all()

    # Iterate through each person-note data set in the PEOPLE_NOTES list
    for data in PEOPLE_NOTES:
        # Create a new 'Person' instance with the provided last name and first name from the data
        new_person = Person(lname=data.get("lname"), fname=data.get("fname"))

        # Iterate through each note and its associated timestamp for the current person
        for content, timestamp in data.get("notes", []):
            # Create a new 'Note' for the current person with the given content and timestamp
            # The timestamp string is converted into a datetime object for proper storage
            new_person.notes.append(
                Note(
                    content = content,
                    timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S"),
                )
            )

        # Add the new person (with their notes) to the session to be saved to the database
        db.session.add(new_person)

    # Commit the changes, saving all the new persons and their notes to the database
    db.session.commit()
