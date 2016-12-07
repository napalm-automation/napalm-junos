#!/usr/bin/env python

# Copyright (c) 2015 eBay.  All Rights Reserved.

from napalm_junos.tests import base


class SampleTestSuite(base.DietTestCase):
    """Sample Test Suite

    This test suite performs setup and teardown functions for this file's
    unit tests. Each unit test class should inherit from this class, and
    implement a single "runTest" function.
    """

    def setUp(self):
        """Perform setup activities

        """

        super(SampleTestSuite, self).setUp()

    def tearDown(self):
        """Perform teardown activities

        """

        super(SampleTestSuite, self).tearDown()


class sample_test(SampleTestSuite):
    """Sample unit test

    """

    def runTest(self):

        self.assertTrue(None in [None])
