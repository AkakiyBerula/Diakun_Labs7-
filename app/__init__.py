from flask import Flask, flash, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

from . import views, models