from flask import Flask, flash, redirect, url_for, render_template
from sqlalchemy import MetaData 
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import config


convention={
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData( naming_convention = convention) 

db = SQLAlchemy(metadata=metadata)
migrate = Migrate()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = "info"
bcrypt = Bcrypt()



def create_app(config_name="default"):
    print(str(config_name))
    """Construct the core application."""
    app = Flask(__name__)
    app.config.from_object(config.get(config_name))
    db.init_app(app)
    migrate.init_app(app,db,render_as_batch=True)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    #api = Api(app)
    with app.app_context():
        # Imports
        from .main import main_blueprint
        app.register_blueprint(main_blueprint, url_prefix='/')

        from .auth import auth_blueprint
        app.register_blueprint(auth_blueprint, url_prefix='/auth')


        from .form_cabinet import form_cabinet_blueprint
        app.register_blueprint(form_cabinet_blueprint, url_prefix='/form_cabinet')

        from .contract_activities import contract_activities_blueprint
        app.register_blueprint(contract_activities_blueprint, url_prefix='/contract_activities')

        from .post import posts_blueprint
        app.register_blueprint(posts_blueprint, url_prefix='/posts')

        from .api import api_blueprint
        app.register_blueprint(api_blueprint, url_prefix='/api')
        
        from .api_v2 import api_v2_blueprint 
        app.register_blueprint(api_v2_blueprint, url_prefix='/api/v2')

        from .ekz import api_ekz_blueprint
        app.register_blueprint(api_ekz_blueprint, url_prefix='/api/diakun')
        
        return app