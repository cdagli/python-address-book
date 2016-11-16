#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.utils.database import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields, post_dump


class Address(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address = db.Column(db.String)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class AddressSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Address
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    person_id = fields.Number(dump_only=True)

    @post_dump(pass_many=True)
    def generate_arrays(self, data, many):
        data = ','.join(str(i.get('address')) for i in data)
        return data
