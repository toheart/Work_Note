from main import db


class User(db.Model):
    __bind_key__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)