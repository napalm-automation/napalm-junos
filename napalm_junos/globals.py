# -*- coding: utf-8 -*-

"""Globals to be used in the JunOS driver."""


class JunOSGlobals:

    # used in:
    #   * get_users
    _JUNOS_CLASS_CISCO_PRIVILEGE_LEVEL_MAP = {
        'super-user': 15,
        'superuser': 15,
        'operator': 5,
        'read-only': 1,
        'unauthorized': 0
    }

    # used in:
    #   * get_users
    _DEFAULT_USER_DETAILS = {
        'level': 0,
        'password': '',
        'sshkeys': []
    }

    # used in:
    #   * get_network_instances
    _NETWORK_INSTANCE_MAP = {
        # key is the value of the `routing-interface`
        # value is the routing instance name, corresponding to OpenConfig standards
        'vrf': 'L3VRF',
        'l2vpn': 'L2VPN'
    }
