#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from flask import Blueprint
from flask import request
from api.utils.responses import response_with
from api.utils import responses as resp
from api.models.person import Person, PersonSchema
from api.models.group import Group, GroupSchema
from api.models.email import Email

route_general = Blueprint("route_general", __name__)


@route_general.route('/v1.0/persons', methods=['POST'])
def create_person():
    """
    Create person endpoint
    ---
    parameters:
        -   in: body
            name: body
            schema:
                id: Person
                required:
                    - first_name
                    - last_name
                    - emails
                    - phones
                    - addresses
                    - groups
                properties:
                    first_name:
                        type: string
                        description: First name of the person
                        default: "John"
                    last_name:
                        type: string
                        description: Last name of the person
                        default: "Doe"
                    emails:
                        type: string
                        description: Person's emails as string separated with commas
                        default: "email1@test.com,email2@test.com,email3@test.com"
                    phones:
                        type: string
                        description: Person's phone numbers as string separated with commas
                        default: "112233,334455,667788"
                    addresses:
                        type: string
                        description: Person's addresses as string separated with commas
                        default: "address1,address2,address3"
                    groups:
                        type: string
                        description: Persons groups as string separated with commas
                        default: "group0,group1,group2"

    responses:
        200:
            description: Person created successfully
            schema:
                id: PersonAddSuccess
                properties:
                    code:
                        type: string
                        description: Short response code
                        default: "success"
                    person:
                        schema:
                            id: Person
        500:
            description: Server error
            schema:
                id: GeneralError
                properties:
                    code:
                        type: string
                        default: "serverError"
                    message:
                        type: string
                        description: Error message
                        default: "Server Error"
    """
    try:
        data = request.get_json()
        loaded, error = PersonSchema().load(data)
        created_person = loaded.create()
        dumped, error = PersonSchema().dump(created_person)
        return response_with(resp.SUCCESS_200, value={'person': dumped})
    except Exception as e:
        logging.error(e)
        return response_with(resp.SERVER_ERROR_500)


@route_general.route('/v1.0/groups', methods=['POST'])
def create_group():
    """
    Create group endpoint
    ---
    parameters:
        -   in: body
            name: body
            schema:
                id: Group
                required:
                    - name
                properties:
                    name:
                        type: string
                        description: name of the group
                        default: "group0"
    responses:
        200:
            description: Group created successfully
            schema:
                id: GroupAddSuccess
                properties:
                    code:
                        type: string
                        description: Short response code
                        default: "success"
                    group:
                        schema:
                            id: GroupExtended
                            properties:
                                id:
                                    type: number
                                name:
                                    type: string
        500:
            description: Server error
            schema:
                id: GeneralError

    """
    try:
        data = request.get_json()
        loaded, error = GroupSchema().load(data)
        created_group = loaded.create()
        dumped, error = GroupSchema().dump(created_group)
        return response_with(resp.SUCCESS_200, value={'group': dumped})
    except Exception as e:
        logging.error(e)
        return response_with(resp.SERVER_ERROR_500)


@route_general.route('/v1.0/groups/<string:name>', methods=['GET'])
def get_group_with_name(name):
    """
    Get group's persons by group name
    ---
    parameters:
        -   in: path
            name: name
            description: Exact name of the group
            required: true
            schema:
                type: string
    responses:
        200:
            description: List of users belongs to group
            schema:
                id: GetGroupSuccess
                properties:
                    code:
                        type: string
                        description: Short response code
                        default: "success"
                    persons:
                        schema:
                            type: array
                            items:
                                schema:
                                    id: Person
        500:
            description: Server error
            schema:
                id: GeneralError
    """
    try:
        fetched = Group.query.filter_by(name=name).first()
        dumped, error = PersonSchema(many=True).dump(fetched.persons)
        return response_with(resp.SUCCESS_200, value={'persons': dumped})
    except Exception as e:
        logging.error(e)
        return response_with(resp.SERVER_ERROR_500)


@route_general.route('/v1.0/persons/<int:id>/groups', methods=['GET'])
def get_person_groups(id):
    """
    Returns groups of a person
    ---
    parameters:
        -   in: path
            name: id
            description: ID of the person
            required: true
            schema:
                type: number
    responses:
        200:
            description: List of the groups that person belongs to
            schema:
                id: UserGroups
                properties:
                    code:
                        type: string
                        description: Short response code
                        default: "success"
                    groups:
                        type: string
                        description: Persons groups as string separated with commas
        500:
            description: Server error
            schema:
                id: GeneralError
    """
    try:
        fetched = Person.query.filter_by(id=id).first()
        dumped, error = PersonSchema(only=["groups"]).dump(fetched)
        return response_with(resp.SUCCESS_200, value=dumped)
    except Exception as e:
        logging.error(e)
        return response_with(resp.SERVER_ERROR_500)


@route_general.route('/v1.0/persons/name/<string:keyword>', methods=['GET'])
def find_person_by_name(keyword):
    """
    Returns a person by his/her first name or surname or both
    ---
    parameters:
        -   in: path
            name: keyword
            description: first name, last name or both
            required: true
            schema:
                type: string
    responses:
        200:
            description: Record for the person with the first name, last name searched
            schema:
                id: PersonAddSuccess
        500:
            description: Server error
            schema:
                id: GeneralError
    """
    try:
        query = Person.query.filter(
            (Person.first_name + ' ' + Person.last_name).like('%' + keyword.lower() + '%')
            )
        fetched = query.first()
        dumped, error = PersonSchema().dump(fetched)
        return response_with(resp.SUCCESS_200, value={'person': dumped})
    except Exception as e:
        logging.error(e)
        return response_with(resp.SERVER_ERROR_500)


@route_general.route('/v1.0/persons/email/<string:keyword>', methods=['GET'])
def find_person_by_email(keyword):
    """
    Returns the person with the email provided
    ---
    parameters:
        -   in: path
            name: keyword
            description: prefix or full email
            required: true
            schema:
                type: string
    responses:
        200:
            description: Record for the person with the email provided
            schema:
                id: PersonAddSuccess
        500:
            description: Server error
            schema:
                id: GeneralError
    """
    query = Person.query.join(Email, Email.person_id == Person.id) \
                        .filter(Email.email.like(keyword.lower() + '%'))
    fetched = query.first()
    dumped, error = PersonSchema().dump(fetched)
    return response_with(resp.SUCCESS_200, value={'person': dumped})
