"""
Test Suite for SOAP client
"""
import os
from basetest import BaseTestCase, BetterTestApp # import this first
from fenixlib.run import application
from util_for_test import correct_environ
import unittest
import mock
from fenixlib import exc
from collections import OrderedDict
from fenixlib.clients.soap_context import ContextClient
from zeep.exceptions import Fault
from config_for_test import OX_CONTEXT_WSDL, OX_USER, CONTEXT_PASSWORD, OX_CERT_VERIFY

class ContextClientTests(BaseTestCase):

    def setUp(self):
        self.zeep_patcher = mock.patch('fenixlib.clients.soap_context.zeep')
        self.mock_zeep = self.zeep_patcher.start()
        self.client = ContextClient(wsdl=OX_CONTEXT_WSDL, auth=(OX_USER, CONTEXT_PASSWORD), cert_verify = OX_CERT_VERIFY)

    def tearDown(self):
        self.zeep_patcher.stop()

    def test_service_proxy(self):
        """WSDL gives us an https port 80 url, test our service proxy fixes that"""
        self.assertTrue(":80" not in self.client.service._binding_options['address'])

    def test_get_context_happy(self):
        expected = {"id": 1, "loginMappings": []}
        self.client.service.getData.return_value = expected
        self.mock_zeep.helpers.serialize_object.return_value = expected
        self.assertEqual(self.client.get_context(1), expected)
        self.assertEqual(self.client.service.getData.call_count, 1)
        self.mock_zeep.helpers.serialize_object.assert_called_with(expected)

    def test_get_unknown_error(self):
        self.client.service.getData.side_effect = [Fault("some failure")]
        self.assertRaises(Fault, self.client.get_context, 1)
        self.assertEqual(self.client.service.getData.call_count, 1)

    def test_get_context_dne(self):
        self.client.service.getData.side_effect = [Fault("Context does not exist")]
        self.assertRaises(exc.ContextNotFound, self.client.get_context, 1)
        self.assertEqual(self.client.service.getData.call_count, 1)

    def test_create_happy(self):
        expected = {"id": 1, "loginMappings": []}
        self.mock_zeep.helpers.serialize_object.return_value = expected
        self.assertEqual(self.client.create_context(expected, {"user_name": "some_admin"}), {"id": 1, "loginMappings": []})
        self.assertEqual(self.client.service.create.call_count, 1)

    def test_create_domain_in_use(self):
        self.client.service.create.side_effect = [Fault("Cannot map 'tyrawr.com' to the newly created context. This mapping is already in use.")]
        self.assertRaises(exc.DomainInUse, self.client.create_context, {"id": 105, "loginMappings": ["tyrawr.com"]}, {"user_name": "some_admin"})
        self.assertEqual(self.client.service.create.call_count, 1)

    def test_create_unknown_error(self):
        self.client.service.create.side_effect = [Fault("some failure")]
        self.assertRaises(Fault, self.client.create_context, {"id": 105, "loginMappings": ["tyrawr.com"]}, {"user_name": "some_admin"})
        self.assertEqual(self.client.service.create.call_count, 1)

    def test_delete_context_happy(self):
        self.client.service.delete.return_value = None
        self.assertEqual(self.client.delete_context(1), None)
        self.assertEqual(self.client.service.delete.call_count, 1)

    def test_delete_context_dne(self):
        self.client.service.delete.side_effect = [Fault("Context does not exist")]
        self.assertRaises(exc.ContextNotFound, self.client.delete_context, 1)
        self.assertEqual(self.client.service.delete.call_count, 1)

    def test_delete_unknown_error(self):
        self.client.service.delete.side_effect = [Fault("some failure")]
        self.assertRaises(Fault, self.client.delete_context, 1)
        self.assertEqual(self.client.service.delete.call_count, 1)

    def test_update_context_happy(self):
        self.client.service.change.return_value = None
        self.assertEqual(self.client.update_context(1, {"loginMappings": ["domain.com"]}), None)
        self.assertEqual(self.client.service.change.call_count, 1)

    def test_update_unknown_error(self):
        self.client.service.change.side_effect = [Fault("some failure")]
        self.assertRaises(Fault, self.client.update_context, 1, {"loginMappings": ["domain.com"]})
        self.assertEqual(self.client.service.change.call_count, 1)

    def test_update_context_dne(self):
        self.client.service.change.side_effect = [Fault("Context does not exist")]
        self.assertRaises(exc.ContextNotFound, self.client.update_context, 1, {"loginMappings": ["domain.com"]})
        self.assertEqual(self.client.service.change.call_count, 1)

    def test_update_domain_in_use(self):
        self.client.service.change.side_effect = [Fault('A mapping with login info "domain.com" already exists in the system!')]
        self.assertRaises(exc.DomainInUse, self.client.update_context, 1, {"loginMappings": ["domain.com"]})
        self.assertEqual(self.client.service.change.call_count, 1)

class ContextGetTests(BaseTestCase):

    def setUp(self):
        self.test_app = BetterTestApp(application, extra_environ=correct_environ)

        self.zeep_patcher = mock.patch('fenixlib.clients.soap_context.zeep')
        self.mock_zeep = self.zeep_patcher.start()

        self.client = ContextClient(wsdl=OX_CONTEXT_WSDL, auth=(OX_USER, CONTEXT_PASSWORD), cert_verify = OX_CERT_VERIFY)


    def test_happy_soap_get(self):
        expected = [OrderedDict([('average_size', 200), ('enabled', True), ('filestoreId', 6), \
                    ('filestore_name', '1_ctx_store'), ('id', 1), ('loginMappings', ['test.com', \
                    'eidevtest.com', 'domain.com']), ('maxQuota', 1024), ('name', '1'), ('readDatabase', \
                    OrderedDict([('clusterWeight', None), ('currentUnits', None), ('driver', None), \
                    ('id', 8), ('login', None), ('master', None), ('masterId', None), ('maxUnits', None), \
                    ('name', None), ('password', None), ('poolHardLimit', None), ('poolInitial', None), \
                    ('poolMax', None), ('read_id', None), ('scheme', 'configdb_11'), ('url', None)])), \
                    ('usedQuota', 0), ('userAttributes', None), ('writeDatabase', \
                    OrderedDict([('clusterWeight', None), ('currentUnits', None), ('driver', None), \
                    ('id', 8), ('login', None), ('master', None), ('masterId', None), ('maxUnits', None), \
                    ('name', None), ('password', None), ('poolHardLimit', None), ('poolInitial', None), \
                    ('poolMax', None), ('read_id', None), ('scheme', 'configdb_11'), ('url', None)]))])]
        self.mock_zeep.helpers.serialize_object.return_value = expected
        self.assertEqual(self.client.list_context_for_domain("domain.com"), expected)

    def test_happy_soap_multi_get(self):
        expected = [OrderedDict([('average_size', 200), ('enabled', True), ('filestoreId', 6),
                                 ('filestore_name', '1_ctx_store'), ('id', 1), ('loginMappings', ['longtest.com',
                                                                                                  'longeidevtest.com',
                                                                                                  'longdomain.com'])]),
                    OrderedDict([('average_size', 200), ('enabled', True), ('filestoreId', 6),
                                 ('filestore_name', '1_ctx_store'), ('id', 1), ('loginMappings', ['test.com',
                                                                                                  'eidevtest.com',
                                                                                                  'domain.com'])])]
        self.mock_zeep.helpers.serialize_object.return_value = expected
        self.assertEqual(self.client.list_context_for_domain("domain.com"), expected)

    def test_500_soap_get(self):
        self.mock_zeep.helpers.serialize_object.side_effect = [Fault("Unknown exception")]
        self.assertRaises(Exception, self.client.list_context_for_domain, "weird")

    def tearDown(self):
        self.zeep_patcher.stop()

if __name__ == '__main__':
    unittest.main()



