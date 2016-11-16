#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from faker import Faker
from api.utils.test_base import BaseTestCase
from api.models.group import Group
from api.models.person import PersonSchema


def add_person(self, data):
    response = self.app.post(
        '/api/v1.0/persons',
        data=json.dumps(data),
        content_type='application/json'
    )
    return response


def add_group(self, data):
    response = self.app.post(
        '/api/v1.0/groups',
        data=json.dumps(data),
        content_type='application/json'
    )
    return response


def get_group(self, group):
    response = self.app.get(
        '/api/v1.0/groups/' + group,
        content_type='application/json'
    )
    return response


def get_person_groups(self, person_id):
    response = self.app.get(
        '/api/v1.0/persons/' + str(person_id) + '/groups',
        content_type='application/json'
    )
    return response


def find_person_by_name(self, keyword):
    response = self.app.get(
        '/api/v1.0/persons/name/' + keyword,
        content_type='application/json'
    )
    return response


def find_person_by_email(self, keyword):
    response = self.app.get(
        '/api/v1.0/persons/email/' + keyword,
        content_type='application/json'
    )
    return response


def generate_test_data():

    for i in range(0, 6):
        Group(name="group" + str(i)).create()

    generate_fake_person('group0,group1,group2').create()
    generate_fake_person('group2,group3,group4').create()
    generate_fake_person('group3,group4,group5').create()


def generate_fake_person(groups):
    fake = Faker()
    test_person = {
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'emails': ','.join(fake.email() for i in range(0, 3)),
        'addresses': ','.join(fake.street_address() for i in range(0, 3)),
        'phones': ','.join(fake.phone_number() for i in range(0, 3)),
        'groups': groups
    }
    loaded, error = PersonSchema().load(test_person)
    return loaded


class TestGroups(BaseTestCase):
    def setUp(self):
        super(TestGroups, self).setUp()

    def test_add_group(self):
        test_group = {
            'name': 'test_group'
        }
        response = add_group(self, test_group)
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue('group' in data)

    def test_get_group_members(self):
        group_to_get = 'group2'
        generate_test_data()
        response = get_group(self, group_to_get)
        self.assertEqual(200, response.status_code)
        data = json.loads(response.data)
        self.assertTrue('persons' in data)
        self.assertEqual(len(data.get('persons')), 2)


class TestPersons(BaseTestCase):
    def setUp(self):
        super(TestPersons, self).setUp()

    def test_add_person(self):
        test_group = {
            'name': 'test_group'
        }
        add_group(self, test_group)
        test_person = {
            'first_name': 'John',
            'last_name': 'Doe',
            'emails': 'email1@test.com,email2@test.com,email3@test.com',
            'addresses': 'address1,address2,address3',
            'phones': '112233,223344,445566',
            'groups': 'test_group'
        }
        response = add_person(self, test_person)
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue('person' in data)

    def test_get_person_groups(self):
        user_to_get = 1
        generate_test_data()
        response = get_person_groups(self, user_to_get)
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue('groups' in data)
        self.assertEqual(len(data.get('groups').split(',')), 3)

    def test_find_person_by_name(self):
        fake_person = generate_fake_person('group0,group1,group2')
        created = fake_person.create()

        # try to find person with first name
        response = find_person_by_name(self, created.first_name)
        self.assertEqual(200, response.status_code)
        data = json.loads(response.data)
        self.assertEqual(created.id, data.get('person').get('id'))

        # try to find person with last name
        response = find_person_by_name(self, created.last_name)
        self.assertEqual(200, response.status_code)
        data = json.loads(response.data)
        self.assertEqual(created.id, data.get('person').get('id'))

        # try to find person with both first name and last name
        response = find_person_by_name(self, created.first_name + ' ' + created.last_name)
        self.assertEqual(200, response.status_code)
        data = json.loads(response.data)
        self.assertEqual(created.id, data.get('person').get('id'))

    def test_find_person_by_email(self):
        fake_person = generate_fake_person('group0,group1,group2')
        created = fake_person.create()

        # Find by exact email
        response = find_person_by_email(self, created.emails[0].email)
        self.assertEqual(200, response.status_code)
        data = json.loads(response.data)
        self.assertEqual(created.id, data.get('person').get('id'))

        # Find by prefix
        response = find_person_by_email(self, created.emails[0].email[:3])
        self.assertEqual(200, response.status_code)
        data = json.loads(response.data)
        self.assertEqual(created.id, data.get('person').get('id'))
