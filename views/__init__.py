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
dbpath = app.root_path.replace("\\", "/")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+dbpath+'/data.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] =True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
print(app.config['SQLALCHEMY_DATABASE_URI'])

db = SQLAlchemy(app)





