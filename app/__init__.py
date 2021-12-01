from flask import Flask, flash, redirect, url_for, render_template
from sqlalchemy import MetaData 
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate

from sqlalchemy import MetaData 

convention={
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData( naming_convention = convention) 

app = Flask(__name__)
app.config.from_object('config')

db=SQLAlchemy(metadata=metadata)
migrate = Migrate(app,db,render_as_batch=True)

bootstrap = Bootstrap(app)
db.init_app(app)

def create_app():
    db.init_app(app)
    migrate.init_app(app, db)
    return app

from . import views, models