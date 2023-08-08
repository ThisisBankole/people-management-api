from datetime import datetime
from config import db, ma



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
 
 
 
 # Create a schema for the Person model which inherits from ma.SQLAlchemyAutoSchema.   
class PersonSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta: # Meta class is used to provide additional configurations for the schema.
        
        # This is how Marshmallow finds attributes in the Person class and learns the types of those attributes so it knows how to serialize and deserialize them.
        model = Person
        load_instance = True
        sqla_session = db.session
        
person_schema = PersonSchema()
people_schema = PersonSchema(many=True)
        
    