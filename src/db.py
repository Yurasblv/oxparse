from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


class Adt(db.Model):

    __tablename__ = "adt"

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
    city = db.Column(db.String(50))
    description = db.Column(db.TEXT())
    beds = db.Column(db.SMALLINT())
    img_url = db.Column(db.String(255))
    date = db.Column(db.Date())
    currency = db.Column(db.Float())

    @property
    def formatted_date(self):
        return self.date.strftime("%d-%m-%Y")
