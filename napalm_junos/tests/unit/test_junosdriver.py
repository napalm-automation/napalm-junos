# -*- coding: utf-8 -*-
# Copyright 2015 Spotify AB. All rights reserved.
#
# The contents of this file are licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.


"""Test Configuration JunOS Network Driver."""


from napalm_base.test.base import TestConfigNetworkDriver
from napalm_base.test.base import TestGettersNetworkDriver
from napalm_junos.junos import JunOSDriver

import lxml
import unittest


class SampleTest(unittest.TestCase):
    """Sample test class."""

    def run_test(self):
        """Sample test method."""

        pass


class TestConfigJunOSDriver(unittest.TestCase, TestConfigNetworkDriver):
    """Test JunOS Config Driver."""

    @classmethod
    def setUpClass(cls):
        """Test setup."""

        hostname = '127.0.0.1'
        username = 'vagrant'
        password = 'vagrant123'
        cls.vendor = 'junos'

        optional_args = {'port': 12203, }
        cls.device = JunOSDriver(hostname,
                                 username,
                                 password,
                                 timeout=60,
                                 optional_args=optional_args)
        cls.device.open()


class TestGetterJunOSDriver(unittest.TestCase, TestGettersNetworkDriver):
    """Test JunOS Driver Getter."""

    @classmethod
    def setUpClass(cls):
        """Test setup."""

        cls.mock = True

        hostname = '192.168.56.203'
        username = 'vagrant'
        password = 'vagrant123'
        cls.vendor = 'junos'

        cls.device = JunOSDriver(hostname, username, password, timeout=60)

        if cls.mock:
            cls.device.device = FakeJunOSDevice()
        else:
            cls.device.open()


class FakeJunOSDevice(object):
    """Fake JunOS Device Class."""

    # Necessary for fake devices.
    ON_JUNOS = True

    def __init__(self):
        self.rpc = FakeRPCObject(self)
        self._conn = FakeConnection(self.rpc)
        self.ON_JUNOS = True  # necessary for fake devices
        self.hostname = 'vsrx'
        self.facts = {
            'domain': None,
            'hostname': 'vsrx',
            'ifd_style': 'CLASSIC',
            '2RE': False,
            'serialnumber': 'beb914a9cca3',
            'fqdn': 'vsrx',
            'virtual': True,
            'switch_style': 'NONE',
            'version': '12.1X47-D20.7',
            'HOME': '/cf/var/home/vagrant',
            'srx_cluster': False,
            'model': 'FIREFLY-PERIMETER',
            'RE0': {
                'status': 'Testing',
                'last_reboot_reason': ('Router rebooted after '
                                       'a normal shutdown.'),
                'model': 'FIREFLY-PERIMETER RE',
                'up_time': '1 hour, 13 minutes, 37 seconds'
            },
            'vc_capable': False,
            'personality': 'SRX_BRANCH'
        }

    def read_txt_file(self, filename):
        with open(filename) as data_file:
            return data_file.read()

    def cli(self, command=''):
        """Mimic CLI commands from text data file."""

        return self.read_txt_file(
            'junos/mock_data/{parsed_command}.txt'.format(
                parsed_command=command.replace(' ', '_')
            )
        )


class FakeRPCObject(object):
    """Fake RPC caller."""

    def __init__(self, device):
        self._device = device

    def __getattr__(self, item):
        self.item = item
        return self

    def response(self, **rpc_args):
        """Return a mocked RPC response."""

        instance = rpc_args.pop('instance', '')

        xml_string = self._device.read_txt_file(
            'junos/mock_data/{}{}.txt'.format(self.item, instance))
        return lxml.etree.fromstring(xml_string)

    def get_config(self, get_cmd=None, filter_xml=None, options={}):

        # get_cmd is an XML tree that requests a specific part of the config
        # E.g.:
        # <configuration>
        #     <protocols>
        #         <bgp>
        #             <group/>
        #         </bgp>
        #     </protocols>
        # </configuration>

        if options is None:
            options = {}

        if get_cmd is not None:
            get_cmd_str = lxml.etree.tostring(get_cmd)
            filename = get_cmd_str.replace('<', '_')\
                                  .replace('>', '_')\
                                  .replace('/', '_')\
                                  .replace('\n', '')\
                                  .replace(' ', '')

        # no get_cmd means it should mock the eznc get_config
        else:
            filename = 'get_config__' + '__'.join(
                ['{0}_{1}'.format(k, v) for k, v in options.items()]
            )

        xml_string = self._device.read_txt_file(
            'junos/mock_data/{filename}.txt'.format(
                filename=filename[0:150]
            )
        )
        return lxml.etree.fromstring(xml_string)

    __call__ = response


class FakeConnectionRPCObject(object):
    """Will make fake RPC requests.

    These are usually directly made via netconf.
    """

    def __init__(self, rpc):
        self._rpc = rpc

    def response(self, non_std_command=None):
        """Fake RPC connection response."""

        class RPCReply(object):
            """Fake RPC Reply response."""

            def __init__(self, reply):
                self._NCElement__doc = reply
        rpc_reply = RPCReply(self._rpc.get_config(get_cmd=non_std_command))
        return rpc_reply

    __call__ = response


class FakeConnection(object):
    """Fake RPC connection."""

    def __init__(self, rpc):
        self.rpc = FakeConnectionRPCObject(rpc)
