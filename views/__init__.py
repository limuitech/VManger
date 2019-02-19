import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from Config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.environ.get('SECRET_KEY') or os.urandom(64)
app.permanent_session_lifetime = timedelta(hours=6)
page_size = 60
tmppath =  app.root_path.replace("\\", "/")+"/../template/"
db = SQLAlchemy(app)





