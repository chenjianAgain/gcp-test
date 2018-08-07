"""
Schema definitions representing a Context
"""

from fenixlib import config
import datetime
from marshmallow import Schema, fields, validate, pre_dump, post_load, post_dump
from fenixlib.schemas.custom_fields import OXDomain


class DomainContext(Schema):
    contextId = fields.Integer(required=True)
    domain = OXDomain(required=True, attribute="domain")

    class Meta:
        strict = True


class Context(Schema):
    """Basic representation of context as seen by clients"""
    contextId = fields.Integer(required=False, attribute="id")
    domains = fields.List(OXDomain(), required=True, attribute="domains")
    theme = fields.String(required=True, validate=validate.OneOf(config.VALID_THEMES))

    @pre_dump
    def denvelope_theme(self, data):
        if "userAttributes" in data and data["userAttributes"] is not None:
            data['theme'] = denvelope_theme(data["userAttributes"])

    @post_load
    def envelope_theme(self, data):
        if "theme" in data and data["theme"] is not None:
            data['userAttributes'] = envelope_theme(data["theme"])

    class Meta:
        strict=True


"""
Schemas for pushing data into app suite. Handles default values
"""


class OXContext(Schema):
    """Internal Data for creating a new context"""
    id = fields.Integer(required=True)
    loginMappings = fields.List(fields.String(), attribute="domains")
    maxQuota = fields.Integer(default=-1, allow_none=True)
    usedQuota = fields.Integer(default=-1)
    enabled = fields.Boolean(default=True)
    userAttributes = fields.Dict(allow_none=True)

    @post_load
    def remove_generic(self, data):
        generic = str(data["id"])
        if generic in data["domains"]:
            data["domains"].remove(generic)

    class Meta:
        strict=True


class AdminUserSchema(Schema):
    """Internal data for admin user required to create a context"""
    name = fields.String(default=None)
    given_name = fields.String(default="Context")
    sur_name = fields.String(default="Admin")
    display_name = fields.String(default="admin")
    primaryEmail = fields.String(default=None, attribute="name")
    email1 = fields.String(default=None, attribute="name")
    mail_enabled = fields.Boolean(default=False)
    password = fields.String(default=None)

    class Meta:
        strict=True


class ContextAccessSchema(Schema):
    """Dynamo (context) table"""
    context_id = fields.String(required=True)
    access_id = fields.String(required=True)
    created = fields.DateTime()
    updated = fields.DateTime(default=None)

    @post_dump
    def new_updated(self, data):
        data['updated'] = str(datetime.datetime.now(tz=datetime.timezone.utc))

    class Meta:
        strict=True


def envelope_theme(theme):
    """Wraps a theme in the userattribute envelope"""
    return {'entries':
                [
                    {
                        'key': 'config',
                        'value':
                            {
                                'entries': [
                                    {
                                        'key': 'io.ox/core//theme',
                                        'value': 'io.ox.{theme}'.format(theme=theme)
                                    }
    ]}}]}


def denvelope_theme(attributes):
    """Remove the theme name from the user attribute object"""
    for entry in attributes["entries"]:
        if entry["key"] == "config":
            for attribute in entry["value"]["entries"]:
                if attribute["key"] == "io.ox/core//theme":
                    return attribute["value"].split('.')[-1]
