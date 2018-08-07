"""
Test Suite for error handlers not necessarily covered by app code
"""
from basetest import BaseTestCase # import this first
import unittest
import mock
from fenixlib import exc
from fenixlib.clients.soap_user import UserClient
from zeep.exceptions import Fault
from util_for_test import context_user_factory
from config_for_test import OX_USER_WSDL, CONTEXT_USER, CONTEXT_PASSWORD, OX_CERT_VERIFY

class UserClientTests(BaseTestCase):

    def setUp(self):
        self.zeep_patcher = mock.patch('fenixlib.clients.soap_user.zeep')
        self.mock_zeep = self.zeep_patcher.start()
        self.client = UserClient(wsdl=OX_USER_WSDL, auth=(CONTEXT_USER, CONTEXT_PASSWORD), cert_verify=OX_CERT_VERIFY)
        self.user = {
            "id": 2,
            "name": "12097e62-adfa-47cf-b3ef-bec932019524",
            "display_name": "localpart",
            "primaryEmail": "localpart@domain.com"
        }

    def tearDown(self):
        self.zeep_patcher.stop()

    def test_service_proxy(self):
        """WSDL gives us an https port 80 url, test our service proxy fixes that"""
        self.assertTrue(":80" not in self.client.service._binding_options['address'])

    # CREATE tests
    def test_create_user_happy(self):
        self.mock_zeep.helpers.serialize_object.return_value = self.user
        self.assertEqual(self.client.create_user(1, self.user, "gd_pim"), self.user)
        self.client.service.createByModuleAccessName.assert_called_with(
            {"id": 1},
            self.user,
            "gd_pim",
            self.client.auth
        )

    def test_create_context_dne_error(self):
        self.client.service.createByModuleAccessName.side_effect = [Fault('Authentication failed')]
        self.assertRaises(exc.ContextNotFound, self.client.create_user, 1, self.user, "gd_pim")
        self.assertEqual(self.client.service.createByModuleAccessName.call_count, 1)

    def test_create_localpart_conflict_error(self):
        self.client.service.createByModuleAccessName.side_effect = [Fault("The displayname is already used")]
        self.assertRaises(exc.UserConflict, self.client.create_user, 1, self.user, "gd_pim")
        self.assertEqual(self.client.service.createByModuleAccessName.call_count, 1)

    def test_create_uuid_conflict_error(self):
        self.client.service.createByModuleAccessName.side_effect = [Fault('User {} already exists in this context'.format(self.user["name"]))]
        self.assertRaises(exc.UserConflict, self.client.create_user, 1, self.user, "gd_pim")
        self.assertEqual(self.client.service.createByModuleAccessName.call_count, 1)

    def test_create_email_conflict_error(self):
        self.client.service.createByModuleAccessName.side_effect = [Fault('Primary mail address "{}" already exists in context {}'.format(self.user["primaryEmail"], 1))]
        self.assertRaises(exc.UserConflict, self.client.create_user, 1, self.user, "gd_pim")
        self.assertEqual(self.client.service.createByModuleAccessName.call_count, 1)

    def test_create_product_dne_error(self):
        self.client.service.createByModuleAccessName.side_effect = [Fault('No such access combination name "gd_pim"')]
        self.assertRaises(exc.NoSuchProduct, self.client.create_user, 1, self.user, "gd_pim")
        self.assertEqual(self.client.service.createByModuleAccessName.call_count, 1)

    def test_create_unknown_error(self):
        self.client.service.createByModuleAccessName.side_effect = [Fault("some failure")]
        self.assertRaises(exc.OXException, self.client.create_user, 1, self.user, "gd_pim")
        self.assertEqual(self.client.service.createByModuleAccessName.call_count, 1)


    # GET/GETALL Tests
    def test_get_user_happy(self):
        self.mock_zeep.helpers.serialize_object.return_value = self.user
        self.assertEqual(self.client.get_user(1, self.user["name"]), self.user)
        self.client.service.getData.assert_called_with(
            {"id": 1},
            {"name": self.user["name"]},
            self.client.auth
        )

    def test_get_unknown_error(self):
        self.client.service.getData.side_effect = [Fault("some failure")]
        self.assertRaises(exc.OXException, self.client.get_user, 1, self.user["name"])
        self.assertEqual(self.client.service.getData.call_count, 1)

    def test_get_context_dne_error(self):
        self.client.service.getData.side_effect = [Fault('Database for context 1 and server BLAH can not be resolved')]
        self.assertRaises(exc.ContextNotFound, self.client.get_user, 1, self.user["name"])
        self.assertEqual(self.client.service.getData.call_count, 1)

    def test_get_user_dne_error(self):
        self.client.service.getData.side_effect = [Fault("No such user {} in context 1".format(self.user['name']))]
        self.assertRaises(exc.UserNotFound, self.client.get_user, 1, self.user["name"])
        self.assertEqual(self.client.service.getData.call_count, 1)

    def test_get_all_user_happy(self):
        self.mock_zeep.helpers.serialize_object.return_value = [context_user_factory(), context_user_factory(), context_user_factory(name="oxadmin")]
        self.client.service.listAll.return_value = [{"id": 1}, {"id": 2}, {"id": 3}]
        response = self.client.get_all_users(1)
        for existing in response:
            self.assertTrue(existing["name"] != "master_user")

    def test_get_all_context_dne_error(self):
        self.client.service.listAll.side_effect = [Fault('Authentication failed')]
        self.assertRaises(exc.ContextNotFound, self.client.get_all_users, 1)
        self.assertEqual(self.client.service.listAll.call_count, 1)

    def test_get_all_unknown_error(self):
        self.client.service.listAll.side_effect = [Fault("some failure")]
        self.assertRaises(exc.OXException, self.client.get_all_users, 1)
        self.assertEqual(self.client.service.listAll.call_count, 1)


    # UPDATE Tests
    def test_update_user_happy(self):
        self.client.service.change.return_value = None
        self.assertEqual(self.client.update_user(1, self.user['name'], self.user), None)
        self.client.service.change.assert_called_with(
            {"id": 1},
            self.user,
            self.client.auth
        )

    def test_update_user_partial_happy(self):
        self.client.service.change.return_value = None
        user = {
            "id": 2,
            "name": "12097e62-adfa-47cf-b3ef-bec932019524",
            "display_name": "localpart",
            "primaryEmail": "localpart@domain.com"
        }
        self.assertEqual(self.client.update_user(1, self.user['name'], user), None)
        self.client.service.change.assert_called_with(
            {"id": 1},
            user,
            self.client.auth
        )

    def test_update_context_dne_error(self):
        self.client.service.change.side_effect = [Fault('The context 1 does not exist!')]
        self.assertRaises(exc.ContextNotFound, self.client.update_user, 1, self.user['name'], self.user)
        self.assertEqual(self.client.service.change.call_count, 1)

    def test_update_user_dne_error(self):
        self.client.service.change.side_effect = [Fault("No such user {} in context 1".format(self.user["name"]))]
        self.assertRaises(exc.UserNotFound, self.client.update_user, 1, self.user['name'], self.user)
        self.assertEqual(self.client.service.change.call_count, 1)

    def test_update_unknown_error(self):
        self.client.service.change.side_effect = [Fault("some failure")]
        self.assertRaises(exc.OXException, self.client.update_user, 1, self.user['name'], self.user)
        self.assertEqual(self.client.service.change.call_count, 1)


    # UPGRADE/DOWNGRADE tests
    def test_update_user_product_happy(self):
        self.client.service.changeByModuleAccessName.return_value = None
        self.assertEqual(self.client.update_user_product(1, self.user["name"], "gd_pim"), None)
        self.client.service.changeByModuleAccessName.assert_called_with(
            {"id": 1},
            {"name": self.user["name"]},
            "gd_pim",
            self.client.auth
        )

    def test_update_product_context_dne_error(self):
        self.client.service.changeByModuleAccessName.side_effect = [Fault('The context 1 does not exist!')]
        self.assertRaises(exc.ContextNotFound, self.client.update_user_product, 1, self.user["name"], "gd_pim")
        self.assertEqual(self.client.service.changeByModuleAccessName.call_count, 1)

    def test_update_product_user_dne_error(self):
        self.client.service.changeByModuleAccessName.side_effect = [Fault("No such user {} in context 1".format(self.user["name"]))]
        self.assertRaises(exc.UserNotFound, self.client.update_user_product, 1, self.user["name"], "gd_pim")
        self.assertEqual(self.client.service.changeByModuleAccessName.call_count, 1)

    def test_update_product_product_dne_error(self):
        self.client.service.changeByModuleAccessName.side_effect = [Fault('No such access combination name "gd_pim"')]
        self.assertRaises(exc.NoSuchProduct, self.client.update_user_product, 1, self.user["name"], "gd_pim")
        self.assertEqual(self.client.service.changeByModuleAccessName.call_count, 1)

    def test_update_product_unknown_error(self):
        self.client.service.changeByModuleAccessName.side_effect = [Fault("some failure")]
        self.assertRaises(exc.OXException, self.client.update_user_product, 1, self.user["name"], "gd_pim")
        self.assertEqual(self.client.service.changeByModuleAccessName.call_count, 1)

    # DELETE Tests
    def test_delete_user_happy(self):
        self.client.service.delete.return_value = None
        self.assertEqual(self.client.delete_user(1, self.user["name"]), None)
        self.client.service.delete.assert_called_with(
            {"id": 1},
            {"name": self.user["name"]},
            self.client.auth
        )

    def test_delete_user_dne_error(self):
        self.client.service.delete.side_effect = [Fault("No such user {user} in context 1".format(user=self.user['name']))]
        self.assertRaises(exc.UserNotFound, self.client.delete_user, 1, self.user["name"])
        self.assertEqual(self.client.service.delete.call_count, 1)

    def test_delete_context_dne_error(self):
        self.client.service.delete.side_effect = [Fault('Authentication failed')]
        self.assertRaises(exc.ContextNotFound, self.client.delete_user, 1, self.user["name"])
        self.assertEqual(self.client.service.delete.call_count, 1)

    def test_delete_unknown_error(self):
        self.client.service.delete.side_effect = [Fault("some failure")]
        self.assertRaises(exc.OXException, self.client.delete_user, 1, self.user["name"])
        self.assertEqual(self.client.service.delete.call_count, 1)


if __name__ == '__main__':
    unittest.main()



