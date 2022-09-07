from src.db import db, migrate
from flask import Flask
from config import DevConfig


def create_app():
    app = Flask(__name__)
    if app.config["ENV"] == "development":
        app.config.from_object(DevConfig)
    print(app.config)
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        db.create_all()
    return app
