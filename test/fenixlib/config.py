import os
import sys
from enum import Enum

API_VERSION = '/v1'
APP_VERSION = os.environ.get("APP_VERSION", "unknown")

# Logging config
LOGGING_DIR = os.environ.get("FENIX_LOGDIR", '/var/log/fenix/')
LOGGING_FILENAME = "fenix_admin_custom.log"
LOGGING_LEVEL = os.environ.get("FENIX_LOG_LEVEL", 'WARNING')

VALID_THEMES = ["godaddy"]

# Enforces authorization on contexts. Only the creator can subsequently read/write
ACCESS_MAP = {
    "workspaceservices.test.client.int.godaddy.com": "bd6017a2-f83a-4e9b-9e24-e443c8a9cba5",
    "testrunner.test.authclient.int.godaddy.com": "86eb655a-886a-49d3-b2af-e1e2f042df34",
    "workspacepanel.test.client.int.godaddy.com": "9c942889-d0b4-457a-9d86-5fb500a7cecd",
    "mailtools.test.authclient.int.godaddy.com": "*"
}

VALID_ISSUER_CNS = ["Go Daddy Secure Certificate Authority - G2",
                    "Starfield Secure Certificate Authority - G2"]
VALID_ISSUER_OUS = ['http://certs.godaddy.com/repository/',
                    'http://certs.starfieldtech.com/repository/']

# Validation Config
VALID_STATUSES = ['active', 'suspended', 'deleted', 'disabled', 'maintenance']
VALID_TRANSITIONS = [
    ('active', 'suspended'), ('suspended', 'active'),
    ('active', 'maintenance'), ('maintenance', 'active'),
    ('active', 'disabled'), ('disabled', 'active'),
]
VALID_LANGUAGES = ['ca_ES', 'cs_CZ', 'da_DK', 'de_DE', 'en_GB', 'en_US', 'es_ES', 'es_MX', 'et_EE', 'fi_FI', 'fr_CA', 'fr_FR',
                   'hu_HU', 'it_IT', 'ja_JP', 'lv_LV', 'nb_NO', 'nl_NL', 'pl_PL', 'pt_BR', 'ro_RO', 'ru_RU', 'sk_SK', 'sv_SE',
                   'zh_CN', 'zh_TW']
# technically features.encryption is totally supported, but features.sharedContent would not work
# any updates of features will be unsupported and return 422
UNSUPPORTED_UPDATES = ("mailbox_uid", "email_address", "aliases")

class NullSig(Enum):
    null = 0
