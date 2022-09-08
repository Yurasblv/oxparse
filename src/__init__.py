from src.db import db, migrate
from flask import Flask
from config import DevConfig
from src.scrapper import grab


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevConfig)
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        db.create_all()
        grab()
    return app
