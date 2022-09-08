"""MODELS FILE"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime


db = SQLAlchemy()
migrate = Migrate()


class Adt(db.Model):
    """Model for adt"""

    __tablename__ = "adt"

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
    city = db.Column(db.String(50))
    description = db.Column(db.TEXT())
    beds = db.Column(db.String(255))
    img_url = db.Column(db.String(255))
    date = db.Column(db.DATE())
    currency = db.Column(db.String(10))
    amount = db.Column(db.Float())

    @staticmethod
    def formatted_date(value):
        """
        Checks formant of input date

        If value cannot be recognized, it returns None

        """
        try:
            date = datetime.strptime(value, "%d/%m/%Y").strftime("%d-%m-%Y")
            date_obj = datetime.strptime(date, "%d-%m-%Y").date()
            return date_obj
        except:
            return None

    @staticmethod
    def check_amount(value):
        """
        Checks formant of input amount

        Remove all commas from sum

        """
        try:
            return float(value.replace(",", ""))
        except:
            print("No amount detected")
            return None
