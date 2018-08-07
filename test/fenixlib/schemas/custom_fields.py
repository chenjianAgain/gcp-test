from marshmallow import validate
from marshmallow import fields
import re


class OXValidatorEmail(validate.Email):

    USER_REGEX = re.compile(
        r"(\A[a-zA-Z0-9!#$+\-^_~'&]{1,64}\Z"
        # quoted-string
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]'
        r'|\\[\001-\011\013\014\016-\177])*"$)', re.IGNORECASE | re.UNICODE)

    DOMAIN_REGEX = re.compile(
        # domain
        r'((?P<DomainParts>[a-zA-Z0-9\-]{1,128}\.)+[a-zA-Z]{2,18}\Z'
        # literal form, ipv4 address (SMTP 4.1.3)
        r'|^\[(25[0-5]|2[0-4]\d|[0-1]?\d?\d)'
        r'(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\]$)', re.IGNORECASE | re.UNICODE)

    def __init__(self, error=None):
        super(OXValidatorEmail, self).__init__(error)


class OXEmail(fields.Email):

    def __init__(self, *args, **kwargs):
        super(OXEmail, self).__init__(*args, **kwargs)
        self.validators[0] =  OXValidatorEmail(error=self.error_messages['invalid'])

    def _validated(self, value):
        if value is None:
            return None
        return OXValidatorEmail(
            error=self.error_messages['invalid']
        )(value)


class CustomDomainValidator(validate.Regexp):

    DOMAIN_REGEX = (
        # domain
        r'((?P<DomainParts>[a-zA-Z0-9\-]{1,128}\.)+[a-zA-Z]{2,18}\Z'
        # literal form, ipv4 address (SMTP 4.1.3)
        r'|^\[(25[0-5]|2[0-4]\d|[0-1]?\d?\d)'
        r'(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\]$)')

    def __init__(self, error=None):
        super(CustomDomainValidator, self).__init__(regex=self.DOMAIN_REGEX, error=error)


class OXDomain(fields.Email):

    default_error_messages = {'invalid': 'Not a valid domain.'}

    def __init__(self, *args, **kwargs):
        super(OXDomain, self).__init__(*args, **kwargs)
        self.validators[0] =  CustomDomainValidator(error=self.error_messages['invalid'])

    def _validated(self, value):
        if value is None:
            return None
        return CustomDomainValidator(
            error=self.error_messages['invalid']
        )(value)