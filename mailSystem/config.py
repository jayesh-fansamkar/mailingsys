import os

uri = os.getenv("DATABASE_URL")
if uri and uri.startswith("postgres://"):
    val = uri.replace("postgres://", "postgresql://", 1)

class Config:
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:hr@localhost/mailingsys'
    SQLALCHEMY_DATABASE_URI = val
    # MAKE DEBUG FALSE
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'sqlalchemy'
