#!/usr/bin/env python
# Copyright (c) 2013 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import uuid

from pip.req import parse_requirements
from setuptools import find_packages
from setuptools import setup

__author__ = 'David Barroso <dbarrosop@dravetech.com>'

install_reqs = parse_requirements('requirements.txt', session=uuid.uuid1())
reqs = [str(ir.req) for ir in install_reqs]


# In python < 2.7.4, a lazy loading of package `pbr` will break
# setuptools if some other modules registered functions in `atexit`.
# solution from: http://bugs.python.org/issue15881#msg170215
try:
    import multiprocessing  # noqa
except ImportError:
    pass


setup(
    setup_requires=['pbr>=1.8'],
    pbr=True,
    name="napalm-junos",
    version="0.4.4",
    packages=find_packages(),
    author="David Barroso, Mircea Ulinic",
    author_email="dbarrosop@dravetech.com, mircea@cloudflare.com",
    description=("Network Automation and Programmability Abstraction "
                 "Layer with Multivendor support"),
    classifiers=[
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
    ],
    url="https://github.com/napalm-automation/napalm-junos",
    include_package_data=True,
    install_requires=reqs
)
