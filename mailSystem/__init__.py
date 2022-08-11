from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

from mailSystem.config import Config

# from models import *


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
app.config['SESSION_SQLALCHEMY'] = db

# session = Session(app)
Session(app)

from mailSystem import routes
