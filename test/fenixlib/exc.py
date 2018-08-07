"""
Custom Exceptions Module
Define all custom exceptions generated within the app here
"""
class UnsupportedUpdate(Exception):
    """Exception for trying to patch unsupported fields"""
    def __init__ (self, bad_fields, *args, **kwargs):
        super(UnsupportedUpdate, self).__init__(*args, **kwargs)
        self.errors = {}
        for field in bad_fields:
            self.errors[field] = [str(self)]

class InvalidHashError(Exception):
    """Raised when there is an issue computing a hash"""
    pass

class UserNotFound(Exception):
    """Simple exception to be raised when a user DNE"""
    pass

class MismatchedUID(Exception):
    """Raised when a client requests a user which matches a specific uid, but there is a mismatch"""
    pass

class ServiceUnavailable(Exception):
    pass

class Forbidden(Exception):
    pass

class Unauthorized(Exception):
    pass

class DataStoreUIDConflict(Exception):
    """Raised when there is a UID collision"""
    pass

class DataStoreEmailConflict(Exception):
    """Raised when there is a email address collision"""
    pass

class DataStoreUnavailable(Exception):
    pass

# App suite exceptions
class OXException(Exception):
    """Generic exception for OX"""
    pass

class ContextNotFound(OXException):
    """Exception for when a context DNE"""
    pass

class UserConflict(OXException):
    """Exception for username already in use"""
    pass

class NoSuchProduct(OXException):
    """Exception for trying to use a product that DNE"""
    def __init__ (self, *args, **kwargs):
        super(NoSuchProduct, self).__init__(*args, **kwargs)
        self.errors = {"productType": [str(self)]}

class ContextException(Exception):
    """Base exception which all context errors inherit from"""
    pass

class ContextAlreadyExists(ContextException):
    """Exception for when a context DNE"""
    pass

class DomainInUse(ContextException):
    """Exception for when a context DNE"""
    pass

class QueryValidation(Exception):
    """Exception for when a query cannot be executed"""

class DoveAdmException(Exception):
    """Unknown responses from doveadm calls"""

class DomainNotFound(Exception):
    """Exception for when a context DNE"""
    pass

