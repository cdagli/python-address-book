#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.utils.database import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields, pre_load, post_dump
from api.models.email import Email, EmailSchema
from api.models.phone import Phone, PhoneSchema
from api.models.address import Address, AddressSchema
from api.models.group import Group, GroupSchema


persons_groups = db.Table('persons_groups',
                          db.Column('group_id', db.Integer, db.ForeignKey('groups.id')),
                          db.Column('person_id', db.Integer, db.ForeignKey('persons.id')))


class Person(db.Model):
    __tablename__ = 'persons'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    emails = db.relationship(Email, backref='Person')
    phones = db.relationship(Phone, backref='Person')
    addresses = db.relationship(Address, backref='Person')
    groups = db.relationship(Group, secondary='persons_groups', backref=db.backref('persons'))

    def create(self):
        groups = []
        for row in self.groups:
            groups.append(self.find_or_create_group(row.name))
        self.groups = groups
        db.session.add(self)
        db.session.commit()
        return self

    def find_or_create_group(self, group_name):
        fetched = Group.query.filter_by(name=group_name).first()
        if not(fetched):
            fetched = Group(name=group_name)
        return fetched


class PersonSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Person
        sqla_session = db.session

    emails = fields.Nested(EmailSchema, many=True)
    phones = fields.Nested(PhoneSchema, many=True)
    addresses = fields.Nested(AddressSchema, many=True)
    groups = fields.Nested(GroupSchema, many=True)

    @pre_load
    def parse_arrays(self, data):
        data['phones'] = [{'number': i} for i in data.get('phones').split(',')]
        data['emails'] = [{'email': i} for i in data.get('emails').split(',')]
        data['addresses'] = [{'address': i} for i in data.get('addresses').split(',')]
        data['groups'] = [{'name': i} for i in data.get('groups').split(',')]
        return data
