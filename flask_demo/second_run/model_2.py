from main import db

class school(object):
    __bind_key__ = 'school'
    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String(80), unique=True)