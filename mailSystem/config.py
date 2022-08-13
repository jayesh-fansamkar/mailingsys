

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:hr@localhost/mailingsys'
    # MAKE DEBUG FALSE
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'sqlalchemy'
