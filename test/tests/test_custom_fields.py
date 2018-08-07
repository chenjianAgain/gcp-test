"""
Test Suite for go daddy custom fields
"""
from basetest import BaseTestCase  #import this first
import unittest
from marshmallow import Schema
from fenixlib.schemas.custom_fields import OXEmail

class OXEmailSchema(Schema):
    user_id = OXEmail()

class CustomFieldsValidationTest(BaseTestCase):

    oxemail_req = OXEmailSchema()
    oxemail_resp = OXEmailSchema()

    def test_happy_oxemail(self):
        result = self.oxemail_req.load({'user_id': 'test@test.com'})
        self.assertEqual(result.data, {'user_id': 'test@test.com'})
        response_data = {'user_id': 'test@test.com'}
        result2 = self.oxemail_resp.dump(response_data).data
        self.assertEqual(result2, {'user_id': 'test@test.com'})

    def test_fail_bad_domain_oxemail(self):
        result = self.oxemail_req.load({'user_id': 'test@invaliddomain'})
        self.assertEqual(result.errors, {'user_id': ['Not a valid email address.']})
        response_data = {'user_id': 'test@invaliddomain'}
        result2 = self.oxemail_resp.dump(response_data).data
        self.assertEqual(result2, {})

    def test_no_value_oxemail(self):
        result = self.oxemail_req.load({'user_id': None})
        self.assertEqual(result.errors, {'user_id': ['Field may not be null.']})
        response_data = {'user_id': None}
        result2 = self.oxemail_resp.dump(response_data).data
        self.assertEqual(result2,  {'user_id': None})

    def test_fail_localpart_length_oxemail(self):
        result = self.oxemail_req.load({'user_id': 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklm@test.com'})
        self.assertEqual(result.errors, {'user_id': ['Not a valid email address.']})
        response_data = {'user_id': 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklm@test.com'}
        result2 = self.oxemail_resp.dump(response_data).data
        self.assertEqual(result2, {})

    def test_fail_domain_length_oxemail(self):
        result = self.oxemail_req.load({'user_id': 'test@123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789.com'})
        self.assertEqual(result.errors, {'user_id': ['Not a valid email address.']})
        response_data = {'user_id': 'test@123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789.com'}
        result2 = self.oxemail_resp.dump(response_data).data
        self.assertEqual(result2, {})

    def test_fail_tld_length_oxemail(self):
        result = self.oxemail_req.load({'user_id': 'test@test.comcomcomcomcomcomZ'})
        self.assertEqual(result.errors, {'user_id': ['Not a valid email address.']})
        response_data = {'user_id': 'test@test.comcomcomcomcomcomZ'}
        result2 = self.oxemail_resp.dump(response_data).data
        self.assertEqual(result2, {})

    def test_subdomains(self):
        result = self.oxemail_req.load({'user_id': 'test@hello.world.co.uk'})
        self.assertEqual(result.data, {'user_id': 'test@hello.world.co.uk'})
        response_data = {'user_id': 'test@hello.world.co.uk'}
        result2 = self.oxemail_resp.dump(response_data).data
        self.assertEqual(result2, {'user_id': 'test@hello.world.co.uk'})


    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':
    unittest.main()
