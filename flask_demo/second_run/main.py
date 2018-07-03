
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def hello():
    return "hello world"

import model_1
import model_2