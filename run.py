from app import create_app
from os import environ

app_launch = create_app(environ.get('FLASK_CONFIG'))

if __name__ == "__main__":
    create_app(config_name='dev').run()