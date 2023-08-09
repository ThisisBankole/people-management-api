from datetime import datetime
from config import db, ma
from marshmallow_sqlalchemy import fields

 #This defines the Note class. 
# Inheriting from db.Model from config.py file gives Note the SQLAlchemy features to connect to the database and access its tables.
class Note(db.Model):
    __tablename__ = "note"
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"))
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
class NoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Note
        load_instance = True
        sqla_session = db.session
        include_fk = True
    

# This defines the Person class. 
# Inheriting from db.Model from config.py file gives Person the SQLAlchemy features to connect to the database and access its tables.
class Person(db.Model):
    __tablename__ = "person"  # This connects the class definition to the person database table.
    id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(32), unique=True)
    fname = db.Column(db.String(32))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 
    # define a timestamp field with a datetime value.
    # The default=datetime.utcnow parameter defaults the timestamp value to the current utcnow value when a record is created. 
    # The onupdate=datetime.utcnow parameter updates the timestamp with the current utcnow value when the record is updated.
    
    # This is to create a relattionshp between the Person table amd the Note table
    notes = db.relationship(
        Note,
        backref="Person",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(Note.timestamp)"
    )
 
 
 
# Here I am creating a blueprint (or a set of instructions) called PersonSchema which is based on ma.SQLAlchemyAutoSchema. 
# This blueprint will help me convert data from a Python object (in this case, a Person object) to a format that can be easily saved or shared (like JSON) and vice versa.
class PersonSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta: # Meta class is used to provide additional configurations for the schema.
        
        # This is how Marshmallow finds attributes in the Person class and learns the types of those attributes so it knows how to serialize and deserialize them.
        model = Person
        load_instance = True
        sqla_session = db.session
        include_relationships = True

    notes = fields.Nested(NoteSchema, many=True) #  I am saying that a Person object can have many Note objects associated with it. The NoteSchema will handle the conversion of these Note objects. The many=True part indicates that there can be multiple Note objects for a single Person.
        
person_schema = PersonSchema()
people_schema = PersonSchema(many=True)
note_schema = NoteSchema()
        
    