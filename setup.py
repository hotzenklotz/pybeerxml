from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys

import pybeerxml

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name = 'pybeerxml',
    packages = ['pybeerxml'],
    version = '1.0.1',
    description = 'A BeerXML Parser',
    author = 'Tom Herold',
    author_email = 'heroldtom@gmail.com',
    url = 'https://github.com/hotzenklotz/pybeerxml',
    download_url = 'https://github.com/hotzenklotz/pybeerxml/tarball/0.1',
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    platforms='any',
    keywords = ['beerxml', 'beer', 'xml', 'brewing'],
    classifiers = [],
    extras_require={
          'testing': ['pytest'],
      }
)