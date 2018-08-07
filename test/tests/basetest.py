import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# os.environ['fenix_user_ENV']='UNIT'
import unittest
import webtest

class BaseTestCase(unittest.TestCase):
    """Base class for all test cases"""

    def __init__(self, *args, **kwargs):
        super(BaseTestCase, self).__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls):

        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

class BetterTestApp(webtest.TestApp):

    """A testapp that prints the body when status does not match."""

    def _check_status(self, status, res):
        if status is not None and status != res.status_int:
            raise webtest.AppError(
                "Bad response: %s (not %s)\n%s", res.status, status, res)
        super(BetterTestApp, self)._check_status(status, res)
