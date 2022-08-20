from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from mailSystem.config import Config


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
app.config['SESSION_SQLALCHEMY'] = db

session = Session(app)

from mailSystem.routes.mainsys import comms
from mailSystem.routes.fashiongrade import shop

app.register_blueprint(shop)
app.register_blueprint(comms)
# from mailSystem import routes
