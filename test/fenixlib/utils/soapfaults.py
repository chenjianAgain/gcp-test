"""
Utility for taking a soap fault and re-raising an appropriate custom exception
"""
from fenixlib import exc

def check_fault(fault, context_id, mailbox_uid=None):
    """
    Interprets the message of a fault and raises a custom exception

    :param fault: a zeep.exceptions.Fault return from open exchange
    :param context_id: The numeric id of the context
    :param mailbox_uid: the uuid identifying the user
    """
    exc_message = str(fault)

    if exc_message == 'Authentication failed':
        # OX gives auth failed when a context DNE. We know the auth is correct so raise not found
        raise exc.ContextNotFound("The context {} does not exist".format(context_id))

    elif exc_message == 'The context {} does not exist!'.format(context_id):
        raise exc.ContextNotFound("The context {} does not exist".format(context_id))

    elif ('Database for context {context_id} and server'.format(context_id=context_id)
          in exc_message and 'can not be resolved' in exc_message):
        # Cryptic way of saying the context DNE
        raise exc.ContextNotFound("The context {} does not exist".format(context_id))

    elif "No such user {user} in context {context_id}".format(user=mailbox_uid, context_id=context_id) in exc_message:
        raise exc.UserNotFound(exc_message)

    elif exc_message == 'The displayname is already used':
        raise exc.UserConflict("The displayName already exists in context")

    elif exc_message == 'User {} already exists in this context'.format(mailbox_uid):
        raise exc.UserConflict("The user uuid {} already exists".format(mailbox_uid))

    elif "Primary mail address" in exc_message and "already exists in context" in exc_message:
        raise exc.UserConflict("The emailAddress already exists in context")

    elif 'No such access combination name' in exc_message:
        raise exc.NoSuchProduct("The given product type does not exist")


    else:
        raise exc.OXException(str(fault))
