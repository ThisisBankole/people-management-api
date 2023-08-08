import pathlib
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# This creates the variable basedir pointing to the directory that the program is running in.
basedir = pathlib.Path(__file__).parent.resolve()
# This uses the basedir variable to create the Connexion app instance and give it the path to the directory that contains your specification file.
connex_app = connexion.App(__name__, specification_dir=basedir)

app = connex_app.app
# This tells SQLAlchemy to use SQLite as the database and a file named people.db in the current directory as the database file.
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'people.db'}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# This initializes SQLAlchemy by passing the app configuration information to SQLAlchemy and assigning the result to a db variable.
db=SQLAlchemy(app)
# This initializes Marshmallow and allows it to work with the SQLAlchemy components attached to the app.
ma=Marshmallow(app)

