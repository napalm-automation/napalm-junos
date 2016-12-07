# Copyright (c) 2015 eBay.  All Rights Reserved.

import unittest


class DietTestCase(unittest.TestCase):
    """Same great taste, less filling.

    DietTestCase performs setup and teardown activities that ALL other unit
    tests should also perform. Each test suite should inherit from
    DietTestCase, and run super().setUp() before running it's own setup
    activities. Same for teardown.
    """

    def setUp(self):
        """Perform setup activies for all unit tests

        """

        pass

    def tearDown(self):
        """Perform teardown activies for all unit tests

        """

        pass
