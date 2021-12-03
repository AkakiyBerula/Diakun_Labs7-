from app import create_app, db

manager = create_app()

if __name__ == "__main__":
    manager.run()