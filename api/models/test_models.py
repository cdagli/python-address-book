#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.utils.test_base import BaseTestCase
from api.models.person import Person, PersonSchema
from api.models.email import Email
from api.models.phone import Phone
from api.models.group import Group
from api.models.address import Address


class TestModels(BaseTestCase):
    def setUp(self):
        super(TestModels, self).setUp()

    def test_create_group(self):
        test_group_name = "test_group"
        Group(name=test_group_name).create()
        fetched = Group.query.filter_by(name=test_group_name).first()
        self.assertEqual(fetched.name, test_group_name)

    def test_create_phone(self):
        test_number = '112233'
        Phone(number=test_number).create()
        fetched = Phone.query.filter_by(number=test_number).first()
        self.assertEqual(fetched.number, test_number)

    def test_create_email(self):
        test_email = "test@test.com"
        Email(email=test_email).create()
        fetched = Email.query.filter_by(email=test_email).first()
        self.assertEqual(fetched.email, test_email)

    def test_create_address(self):
        test_address = "test street no 1"
        Address(address=test_address).create()
        fetched = Address.query.filter_by(address=test_address).first()
        self.assertEqual(fetched.address, test_address)

    def test_create_person(self):
        test_first_name = "John"
        test_last_name = "Doe"
        Person(first_name=test_first_name, last_name=test_last_name).create()
        fetched = Person.query.filter_by(first_name=test_first_name).first()
        self.assertEqual(fetched.first_name, test_first_name)
        self.assertEqual(fetched.last_name, test_last_name)


class TestSchemas(BaseTestCase):
    def setUp(self):
        super(TestSchemas, self).setUp()
        self.test_person = {
            'first_name': 'John',
            'last_name': 'Doe',
            'emails': 'email1@test.com,email2@test.com,email3@test.com',
            'addresses': 'address1,address2,address3',
            'phones': '112233,223344,445566',
            'groups': 'group1,group2'
        }

    def test_person_schema_load(self):
        loaded, error = PersonSchema().load(self.test_person)
        self.assertEqual(loaded.first_name, self.test_person.get('first_name'))
        self.assertEqual(loaded.last_name, self.test_person.get('last_name'))
        self.assertTrue(type(loaded.phones), list)
        self.assertTrue(type(loaded.emails), list)
        self.assertTrue(type(loaded.addresses), list)
        self.assertTrue(type(loaded.groups), list)

    def test_person_schema_dump(self):
        test_person = self.test_person.copy()
        loaded, error = PersonSchema().load(self.test_person)
        person = loaded.create()
        dumped, error = PersonSchema(many=False).dump(person)
        self.assertEqual(error, {})
        self.assertEqual(dumped.get('addresses'), test_person.get('addresses'))
        self.assertEqual(dumped.get('phones'), test_person.get('phones'))
        self.assertEqual(dumped.get('emails'), test_person.get('emails'))
