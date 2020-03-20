import os
from flask_sqlalchemy import SQLAlchemy

from pay import app


basedir = os.path.abspath(os.path.dirname(__file__))
session_options = {'autocommit': False, 'autoflush': False}
db = SQLAlchemy(app, session_options=session_options)

class Payments(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Float)
    currency = db.Column(db.String(3))
    payment_id = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)
    date_time = db.Column(db.DateTime)

    def __init__(self, amount, currency, payment_id, description, date_time):
        self.amount = amount
        self.currency = currency
        self.payment_id = payment_id
        self.description = description
        self.date_time = date_time


    def __repr__(self):
        return "Payment {} {};{};{};{};{}".format(self.id,
                                               self.amount,
                                               self.currency,
                                               self.payment_id,
                                               self.description,
                                               self.date_time)


db.create_all()
