from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String, unique=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String)
    matched = db.Column(db.Boolean, default=False)

class MatchResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_id_1 = db.Column(db.Integer, db.ForeignKey('transaction.id'))
    transaction_id_2 = db.Column(db.Integer, db.ForeignKey('transaction.id'))
    status = db.Column(db.String)  # e.g., 'matched', 'exception'
    approved = db.Column(db.Boolean, default=False)

