import os


class Config:
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:hr@localhost/mailingsys'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # MAKE DEBUG FALSE
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'sqlalchemy'
