from config import db
from flask import abort, make_response
from models import Person, people_schema, person_schema

# This is a function used for returning the list of people. GET/api/people | 
# I am using people_schema which is an instance of the Marshmallow PersonSchema class (models.py) that was created with the parameter many=True. 
# With this parameter you tell PersonSchema to expect an iterable to serialize. 
# This is important because the people variable contains a list of database items.
def read_all():
    people = Person.query.all()
    return people_schema.dump(people)



#This is a function used for creating a person. 
# This receives a person object. This object must contain lname, which must not exist in the database already. 
# If the last name is unique, then I deserialize the person object as new_person and add it to db.session. 
# Once I commit new_person to the database, the database engine assigns a new primary key value and a UTC-based timestamp to the object.

def create(person):
    lname = person.get("lname")
    existing_person = Person.query.filter(Person.lname == lname).one_or_none()
    
    if existing_person is None:
        new_person = person_schema.load(person, session=db.session)
        db.session.add(new_person)
        db.session.commit()
        return person_schema.dump(new_person) , 201
    else:
        abort(
            406,
            f"Person with last name {lname} already exist"
        )
        
        
#This is a function used for returning just one person in a list. GET/api/people/lname
# I am using lname in the query’s .filter() method to get one user that matches the criteria. 
# I use the .one_or_none() method to get one person, or return None if no match is found.
        
def read_one(lname):
    person = Person.query.filter(Person.lname == lname).one_or_none()
    if person is not None:
        return person_schema.dump(person), 200
    else:
        abort(
            404,
            f"user with last name {lname} do not exist"
        )
        
        
#This is a function used for updating just one person in a list       
def update(lname, person):
    existing_person = Person.query.filter(Person.lname == lname).one_or_none()
    if existing_person:
        update_person = person_schema.load(person, session=db.session)
        existing_person.fname = update_person.fname
        db.session.merge(existing_person)
        db.session.commit()
        return person_schema.dump(existing_person), 201
    else:
        abort(
            406,
            f"Person with last name {lname} do not exist"
        )
        
    
#This is a function used for deleting person from a list

def delete(lname):
    existing_person = Person.query.filter(Person.lname == lname).one_or_none()
    if existing_person:
        db.session.delete(existing_person)
        db.session.commit()
        
        return make_response(
            f"{lname} successfully deleted", 200
        )
    else:
        abort(
            406,
            f"Person with last name {lname} not found"
        )