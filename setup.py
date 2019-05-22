#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import yowsup
import platform
import sys

deps = [
    'appdirs==1.4.3',
    'asn1crypto==0.24.0',
    'certifi==2019.3.9',
    'cffi==1.12.3',
    'cryptography==2.6.1',
    'dissononce==0.34.3',
    'enum34==1.1.6',
    'ipaddress==1.0.22',
    'protobuf==3.7.1',
    'pycparser==2.19',
    'python-axolotl-curve25519==0.4.1.post2',
    'six==1.10.0',
    'transitions==0.6.9',
    'consonance==0.1.2',
    'argparse',
    'python-axolotl==0.2.2'
]

if sys.version_info < (2, 7):
    deps.append('importlib')

if platform.system().lower() == "windows":
    deps.append('pyreadline')
else:
    try:
        import readline
    except ImportError:
        deps.append('readline')

setup(
    name='yowsup',
    version=yowsup.__version__,
    url='http://github.com/tgalal/yowsup/',
    license='GPL-3+',
    author='Tarek Galal',
    tests_require=[],
    install_requires = deps,
    scripts = ['yowsup-cli'],
    #cmdclass={'test': PyTest},
    author_email='tare2.galal@gmail.com',
    description='The WhatsApp lib',
    #long_description=long_description,
    packages= find_packages(),
    include_package_data=True,
    data_files = [('yowsup/common', ['yowsup/common/mime.types'])],
    platforms='any',
    #test_suite='',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        #'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ],
    #extras_require={
    #    'testing': ['pytest'],
    #}
)
