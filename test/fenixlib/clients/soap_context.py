"""
Definition of Soap Client used by all methods
Handles caching of wsdl globally in memory
A requests session exists through the lifetime of the client
"""
import zeep
from fenixlib import exc
from requests import Session
from zeep.exceptions import Fault
from zeep.cache import InMemoryCache
from fenixlib.schemas.context import AdminUserSchema

_cache = InMemoryCache(timeout=86400)
admin_schema = AdminUserSchema()

class ContextClient(object):

    def __init__(self, wsdl=None, auth=(None, None), cert_verify=None):
        session = Session()
        session.verify = cert_verify

        self.client = zeep.Client(wsdl,
                                  transport=zeep.transports.Transport(cache=_cache, session=session))
        self.auth = self.client.get_type("ns5:Credentials")(login=auth[0],
                                                            password=auth[1])
        self.service = self.client.create_service(self.client.service._binding.name,
                                                  self.client.service._binding_options['address'].replace(":80", "", 1))

    def get_context(self, context_id):
        """
        Fetches data for a context

        :param context_id: The numeric id of the context
        :return: An OrderedDict with all information about the context
        """
        try:
            return zeep.helpers.serialize_object(
                self.service.getData({"id": context_id}, self.auth)
            )
        except Fault as exceptional:
            if str(exceptional) == 'Context does not exist':
                raise exc.ContextNotFound("The context {} does not exist".format(context_id))
            else:
                raise exceptional

    def list_context_for_domain(self, domain):
        """
        Fetches context record associated with a domain name

        :param domain: The domain name to be looked up
        :return: A dict containing the context record
        """
        try:
            return zeep.helpers.serialize_object(
                self.service.list(domain, self.auth)
            )
        except Fault as exceptional:
                raise exceptional

    def create_context(self, context, admin_user):
        """
        Creates a context

        :param context: A dictionary representing the new context
        :param admin_user: A dictionary representing context admin
        """
        try:
            return zeep.helpers.serialize_object(
                self.service.create(context, admin_user, self.auth)
            )
        except Fault as exceptional:
            exc_message = str(exceptional)
            if "This mapping is already in use" in exc_message:
                raise exc.DomainInUse(exc_message)
            else:
                raise exceptional

    def delete_context(self, context_id):
        """
        Delete a context

        :param context_id: The numeric id of the context
        """
        try:
            self.service.delete({"id": context_id}, self.auth)
        except Fault as exceptional:
            if str(exceptional) == 'Context does not exist':
                raise exc.ContextNotFound("The context {} does not exist".format(context_id))
            else:
                raise exceptional

    def update_context(self, context_id, context):
        """
        Update a context

        :param context_id: The numeric id of the context
        :param context: the new context information to update to
        """
        context["id"] = str(context_id)
        if "loginMappings" in context and context["id"] not in context["loginMappings"]:
            context["loginMappings"].append(context["id"])
        try:
            self.service.change(context, self.auth)
        except Fault as exceptional:
            exc_message = str(exceptional)
            if exc_message == 'Context does not exist':
                raise exc.ContextNotFound("The context {} does not exist".format(context_id))
            elif "already exists in the system!" in exc_message:
                raise exc.DomainInUse(exc_message)
            else:
                raise exceptional
