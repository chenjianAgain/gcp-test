import os
from ast import literal_eval

OX_USER = "master_user"
OX_PASSWORD = "MASTER_PASSWORD"
CONTEXT_USER = "context_user"
CONTEXT_PASSWORD = "CONTEXT_PASSWORD"
OX_CONTEXT_WSDL = "http://context_service.wsdl"
OX_USER_WSDL = "http://user_service.wsdl"

# need to evaluate the bool of a env string
OX_CERT_VERIFY = literal_eval(os.environ.get("OX_CERT_VERIFY", "False"))

# App suite USERS config
OX_RELAY_SERVER = "smtp.test"
OX_USER_PASSWORDS = "user_password"
OX_IMAP_SERVER = 'localhost'
OX_IMAP_PORT = 143
