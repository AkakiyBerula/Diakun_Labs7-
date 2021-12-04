from app import create_app, db

manager = create_app(config_name="dev")

if __name__ == "__main__":
    manager.run()