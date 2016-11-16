#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.utils.database import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields, post_dump


class Email(db.Model):
    __tablename__ = 'emails'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class EmailSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Email
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    person_id = fields.Number(dump_only=True)

    @post_dump(pass_many=True)
    def generate_arrays(self, data, many):
        data = ','.join(str(i.get('email')) for i in data)
        return data
