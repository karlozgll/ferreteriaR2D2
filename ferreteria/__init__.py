import os

from flask import Flask, request
from flask import render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Sequence
from werkzeug.utils import redirect
from flask_cors import CORS
app = Flask(__name__)
cors = CORS(app)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://postgres:karlozgll@127.0.0.1:5432/ferreteria'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

from ferreteria import routes