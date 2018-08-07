from fenixlib import config
import datetime
from marshmallow import Schema, post_dump, fields, validate

class ImapUser(Schema):
    # Operational Specific
    uid = fields.UUID(required=True, attribute="mailbox_uid")
    quota_bytes = fields.Integer(required=True)
    smtp_relays = fields.Integer(required=True)
    status = fields.String(required=True, validate=validate.OneOf(config.VALID_STATUSES))
    access_id = fields.String(required=True)
    created = fields.DateTime()
    updated = fields.DateTime(default=None)
    context_id = fields.Integer()
    # Auth Specific
    sso_emailid = fields.String()
    sso_salt = fields.String(default=None, allow_none=True)
    sso_auth = fields.String(default=None, allow_none=True)
    imap_auth = fields.String(default=None, allow_none=True)
    smtp_auth = fields.String(default=None, allow_none=True)
    # Only exist when a user is status deleted
    delete_date = fields.Integer()
    delete_request_date = fields.DateTime()

    @post_dump
    def new_updated(self, data):
        data['updated'] = str(datetime.datetime.now(tz=datetime.timezone.utc))

    class Meta:
        strict = True
