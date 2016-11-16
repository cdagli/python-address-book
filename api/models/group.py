#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.utils.database import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields, post_dump


class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class GroupSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Group
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    name = fields.String(required=True)

    @post_dump(pass_many=True)
    def generate_arrays(self, data, many):
        if many:
            data = ','.join(i.get('name') for i in data)
        return data
