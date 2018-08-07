"""
Definition of Soap Client used by all methods
Handles caching of wsdl globally in memory
A requests session exists through the lifetime of the client
"""
import zeep
from requests import Session
from zeep.exceptions import Fault
from zeep.cache import InMemoryCache
from fenixlib.utils.soapfaults import check_fault

_cache = InMemoryCache(timeout=86400)

class UserClient(object):

    def __init__(self, wsdl=None, auth=(None, None), cert_verify=None):

        session = Session()
        session.verify = cert_verify

        self.client = zeep.Client(wsdl,
                                  transport=zeep.transports.Transport(cache=_cache, session=session))
        self.auth = self.client.get_type("ns5:Credentials")(login=auth[0],
                                                            password=auth[1])
        self.service = self.client.create_service(self.client.service._binding.name,
                                                  self.client.service._binding_options['address'].replace(":80", "", 1))
        self.user = auth[0]

    def create_user(self, context_id, user, product_type):
        """
        Create a new user in a context

        :param context_id: The numeric id of the context
        :param user: A ContextUser dict
        :param product_type: string representing the product type (sku) they have
        :return: an OrderedDict representing the user created
        """
        try:
            return zeep.helpers.serialize_object(
                self.service.createByModuleAccessName(
                    {"id": context_id},
                    user,
                    product_type,
                    self.auth
                )
            )
        except Fault as exceptional:
            check_fault(exceptional, context_id, user["name"])



    def update_user(self, context_id, mailbox_uid, user_diff):
        """
        Create a new user in a context

        :param context_id: The numeric id of the context
        :param user_diff: A ContextUser dict containing only parameters to update
        """
        user_diff['name'] = mailbox_uid
        try:
            self.service.change(
                {"id": context_id},
                user_diff,
                self.auth
            )
        except Fault as exceptional:
            check_fault(exceptional, context_id, mailbox_uid)


    def update_user_product(self, context_id, mailbox_uid, product_type):
        """
        Change a users capabilities

        :param context_id: The numeric id of the context
        :param mailbox_uid: the uuid identifying the user
        :param product_type: string representing the product type (sku) to change to
        """
        try:
            return self.service.changeByModuleAccessName(
                {"id": context_id},
                {"name": mailbox_uid},
                product_type,
                self.auth
            )
        except Fault as exceptional:
            check_fault(exceptional, context_id, mailbox_uid)

    def get_all_users(self, context_id):
        """
        Fetches all users in a context

        :param context_id: The numeric id of the context
        :return: a list of all users in the context
        """
        exclude_users = False
        include_guests = False
        try:
            response = self.service.listAll({"id": context_id}, self.auth, include_guests, exclude_users)
            id_list = [{"id": user["id"]} for user in response]
            output = zeep.helpers.serialize_object(
                self.service.getMultipleData({"id": context_id}, id_list, self.auth)
            )
            for user in output:
                if user["name"] == self.user:
                    output.remove(user)
            return output
        except Fault as exceptional:
            check_fault(exceptional, context_id)

    def get_user(self, context_id, mailbox_uid):
        """
        Fetches a specific user in a context

        :param context_id: The numeric id of the context
        :param mailbox_uid: the uuid identifying the user
        :return: an OrderedDict representing the user
        """
        try:
            return zeep.helpers.serialize_object(
                self.service.getData(
                    {"id": context_id},
                    {"name": mailbox_uid},
                    self.auth
                )
            )
        except Fault as exceptional:
            check_fault(exceptional, context_id, mailbox_uid)


    def delete_user(self, context_id, mailbox_uid):
        """
        Delete a user from a context

        :param context_id: The numeric id of the context
        :param mailbox_uid: the uuid identifying the user
        """
        try:
            self.service.delete(
                {"id": context_id},
                {"name": mailbox_uid},
                self.auth
            )
        except Fault as exceptional:
            check_fault(exceptional, context_id, mailbox_uid)
