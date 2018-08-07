"""
Utilities for testing
Some general utilities for testing - mostly related to users, schemas, and datastore
FakeDataStore - a dictionary based datastore emulator
user_entity_factory - a factory which takes a dictionary of user data and returns a datastore entity
User factories - A collection of dict-factories which represent the SAME user as it appears to clients
    and two servers (datastore and app suite). Also, the internal user factory represents the internal
    representation of all possible user properties. That model never travels over the wire.
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import datetime
from fenixlib import exc
from fenixlib.schemas.user_dovecot import ImapUser

imap_user_schema = ImapUser()

def user_resource_factory(shared_enabled=False, encryption_enabled=False):
    """Representation of a user as it appears to clients"""
    data = {
        "mailboxUid": "fef02d18-407e-4530-8484-354e8262ac93",
        "givenName": "tyráwr",
        "surName": "durden",
        "displayName": "rawr",
        "emailAddress": "test@domain.com",
        "language": "en_US",
        "aliases": [],
        "quotaBytes": 2000000000,
        "smtpRelays": 500,
        "status": "active",
        "features": {
            "encryption": encryption_enabled,
            "sharedContent": shared_enabled
        }
    }
    return data

def imap_user_data_factory(mailbox_uid="fef02d18-407e-4530-8484-354e8262ac93", status="active"):
    """Representation of a user in datastore for dovecot backend"""
    result = {
        "uid": mailbox_uid,
        "quota_bytes": 2000000000,
        "smtp_relays": 500,
        "status": status,
        'context_id': 1,
        "access_id": "86eb655a-886a-49d3-b2af-e1e2f042df34",
        "sso_emailid": "0f8c7b542b8cfd0cba270e0cdfb57b6da9ffa2040449b09260493955dc08ff0c86ecf71a59ced184",
        "sso_salt": "saltycrypto",
        "sso_auth": "GOODHASH",
        "imap_auth": "BADHASH",
        "smtp_auth": "WORSEHASH",
        "created": "2018-03-01 08:00:00+00:00",
    }
    if status == "deleted":
        result["delete_request_date"] = "2018-03-30 08:00:00+00:00"
        result["delete_date"] = 1520236800
    return result

def deleted_user_data_factory():
    """Representation of a soft delete cleanup record"""
    return {
        "uid": "fef02d18-407e-4530-8484-354e8262ac93",
        "quota_bytes": 2000000000,
        "smtp_relays": 500,
        "status": "deleted",
        "access_id": "86eb655a-886a-49d3-b2af-e1e2f042df34",
        "sso_emailid": "0f8c7b542b8cfd0cba270e0cdfb57b6da9ffa2040449b09260493955dc08ff0c86ecf71a59ced184",
        "sso_salt": "saltycrypto",
        "sso_auth": "GOODHASH",
        "imap_auth": "BADHASH",
        "smtp_auth": "WORSEHASH",
        "created": "2018-03-01 08:00:00+00:00",
        'context_id': 1,
        'delete_request_date': "2018-03-30 08:00:00+00:00",
        'delete_date': 1520236800,
    }

def context_user_factory(features=None, name='fef02d18-407e-4530-8484-354e8262ac93'):
    """Representation of a user in app suite"""
    data = {
        'imapServer': 'localhost',
        'primaryEmail': 'test@domain.com',
        'imapLogin': 'test@domain.com',
        'folderTree': 1,
        'imapPort': 143,
        'mailenabled': True,
        'given_name': 'tyráwr',
        'email1': 'test@domain.com',
        'smtpServer': 'relay.secureserver.net',
        'password': 'password',
        'language': 'en_US',
        'aliases': ['test@domain.com'],
        'sur_name': 'durden',
        'display_name': 'rawr',
        'name': name,
        'defaultSenderAddress': 'test@domain.com'
    }
    if features is not None:
        entries = []
        # !! order of append matters here - must match code
        if "encryption" in features:
            xml_bool = "true" if features['encryption'] else "false"
            entries.append({
                'key': 'com.openexchange.capability.guard-mail',
                'value': xml_bool
            })
        if "sharedContent" in features:
            xml_bool = "true" if features['sharedContent'] else "false"
            entries.append({
                'key': 'com.openexchange.capability.shared_content',
                'value': xml_bool
            })
        data['userAttributes'] = {'entries': [{'value': {'entries': entries}, 'key': 'config'}]}
    return data

def internal_user_factory():
    """Representation of the user within Fenix - a union of all other representations"""
    return {
        'aliases': ['test@domain.com'],
        'access_id': "86eb655a-886a-49d3-b2af-e1e2f042df34",
        'created': datetime.datetime(2018, 2, 15, 9, 11, 17, 278791),
        'display_name': 'rawr',
        'email_address': 'test@domain.com',
        'folderTree': 1,
        'context_id': 1,
        'given_name': 'tyráwr',
        'imapPort': 143,
        'imapServer': 'localhost',
        'imap_auth': 'BADHASH',
        'language': 'en_US',
        'mailbox_uid': 'fef02d18-407e-4530-8484-354e8262ac93',
        'mailenabled': True,
        'password': 'password',
        'product': 'gd_pim',
        'quota_bytes': 2000000000,
        'smtpServer': 'relay.secureserver.net',
        'smtp_auth': 'WORSEHASH',
        'smtp_relays': 500,
        'sso_auth': 'GOODHASH',
        'sso_emailid': '0f8c7b542b8cfd0cba270e0cdfb57b6da9ffa2040449b09260493955dc08ff0c86ecf71a59ced184',
        'sso_salt': 'saltycrypto',
        'status': 'active',
        'sur_name': 'durden'
    }

def mock_get_user_dyna(mailboxUID):
    id_dict = {"8b6daacf-6fe6-4fdb-95d6-860bc57aac2e": "deleted",
               "a660aefd-44a1-4c9f-afdf-0ffdf33f0d9d": "active",
               "7263ad91-98ee-4e70-b9cb-630f17ff6987": "suspended",
               "bf5e1a6a-4694-479f-be37-ea9ab725df93": "maintenance",
               "da0f056d-5ebc-468a-ad0d-34c1a8433eb3": "disabled"
               }
    if mailboxUID in id_dict:
        return imap_user_data_factory(mailboxUID, id_dict[mailboxUID])
    else:
        raise exc.UserNotFound("No users exist within the specified context")

def mock_get_user_soap(contextId, mailboxUID):
    id_dict = {"8b6daacf-6fe6-4fdb-95d6-860bc57aac2e": "deleted",
               "a660aefd-44a1-4c9f-afdf-0ffdf33f0d9d": "active",
               "7263ad91-98ee-4e70-b9cb-630f17ff6987": "suspended",
               "bf5e1a6a-4694-479f-be37-ea9ab725df93": "maintenance",
               "da0f056d-5ebc-468a-ad0d-34c1a8433eb3": "disabled"
               }
    if mailboxUID in id_dict:
        return context_user_factory(mailboxUID, id_dict[mailboxUID])
    else:
        raise exc.UserNotFound("User Not Found")

def mock_contexts(contextId):
    contextlist = [
        [context_user_factory(name="8b6daacf-6fe6-4fdb-95d6-860bc57aac2e"), context_user_factory(name="a660aefd-44a1-4c9f-afdf-0ffdf33f0d9d")],
        [context_user_factory(name="7263ad91-98ee-4e70-b9cb-630f17ff6987"), context_user_factory(name="bf5e1a6a-4694-479f-be37-ea9ab725df93"), context_user_factory(name="6e8ebd6c-8986-4965-86e9-0b1568756bf8"), context_user_factory(name="da0f056d-5ebc-468a-ad0d-34c1a8433eb3")]
    ]
    if 0 < contextId <= 2:
        return contextlist[contextId-1]
    return []

correct_environ = {
    "VERIFIED": "SUCCESS",
    "SUBJECT_DN": "CN=testrunner.test.authclient.int.godaddy.com,OU=Domain Control Validated",
    "ISSUER_DN": "CN=Go Daddy Secure Certificate Authority - G2,OU=http://certs.godaddy.com/repository/,O=GoDaddy.com\\, Inc.,L=Scottsdale,ST=Arizona,C=US",
}
