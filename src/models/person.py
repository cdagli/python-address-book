#!/usr/bin/env python
from api.utils.database import db


class Person(db.Model):
    __tablename__ = 'persons'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    addresses = db.Column(db.DateTime, server_default=db.func.now())
    emails = db.relationship('Book', backref='Author')
    phones = db.Column(db.String)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
