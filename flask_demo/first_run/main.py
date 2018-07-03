from flask import Flask
from config import DevConfig
from flask_sqlalchemy import SQLAlchemy

# 初始化app
app = Flask(__name__)
# 导入app的相关配置项
app.config.from_object(DevConfig)
# 初始化ORM模型
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return "<User '{}'>".format(self.username)




@app.route('/')
def home():
    return "Hello world"

